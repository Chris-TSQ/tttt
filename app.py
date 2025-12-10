import os
import io
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file, render_template_string
from flask_cors import CORS
import mysql.connector
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

app = Flask(__name__)
CORS(app)

# Disable debug mode in production
app.config['DEBUG'] = os.getenv("FLASK_DEBUG", "False").lower() == "true"

GENRE_MAP = {
    "剧情": "Drama", "喜剧": "Comedy", "动作": "Action", "爱情": "Romance",
    "科幻": "Sci-Fi", "动画": "Animation", "惊悚": "Thriller", "恐怖": "Horror",
    "犯罪": "Crime", "冒险": "Adventure", "奇幻": "Fantasy", "战争": "War",
    "历史": "History", "悬疑": "Mystery", "音乐": "Music", "歌舞": "Musical",
    "纪录片": "Documentary", "西部": "Western", "家庭": "Family",
    "传记": "Biography", "武侠": "Martial Arts", "短片": "Short Film", "运动": "Sports"
}

REGION_MAP = {
    "中国大陆": "Mainland China", "香港": "Hong Kong", "台湾": "Taiwan",
    "美国": "USA", "日本": "Japan", "韩国": "Korea", "法国": "France",
    "英国": "UK", "德国": "Germany", "意大利": "Italy", "西班牙": "Spain",
    "加拿大": "Canada", "澳大利亚": "Australia", "西德": "West Germany"
}

def remove_chinese(text):
    """Remove all Chinese characters from text"""
    if pd.isna(text) or not text:
        return ""
    return re.sub(r"[\u4e00-\u9fff]", "", str(text)).strip()

def translate_text(text, mapping):
    """Translate Chinese text using mapping dictionary"""
    if pd.isna(text) or not text:
        return ""
    result = str(text)
    for cn, en in mapping.items():
        result = result.replace(cn, en)
    return remove_chinese(result).strip()

def split_genres(genre_string):
    """Split genre string by various separators"""
    if pd.isna(genre_string) or not genre_string:
        return []
    genres = re.split(r'[/,、]', str(genre_string))
    return [g.strip() for g in genres if g.strip()]

def get_db_connection():
    """Create database connection with error handling"""
    try:
        return mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset="utf8mb4",
            ssl_disabled=True
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Douban Movies</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; margin: 20px; background: #f5f5f5; }
            h1 { text-align: center; color: #333; }
            .plot { background: white; padding: 20px; margin: 20px auto; 
                    border-radius: 8px; max-width: 1400px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            img { width: 100%; height: auto; border-radius: 4px; }
            .error { color: red; padding: 10px; background: #fee; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>🎬 Douban Top 100 Movies Analysis</h1>
        <div class="plot">
            <h2>1. Average Rating by Genre</h2>
            <img src="/plots/avg_rating_by_genre.png" onerror="this.parentElement.innerHTML='<p class=error>Plot failed to load</p>'">
        </div>
        <div class="plot">
            <h2>2. Number of Movies per Genre</h2>
            <img src="/plots/movie_count_by_genre.png" onerror="this.parentElement.innerHTML='<p class=error>Plot failed to load</p>'">
        </div>
        <div class="plot">
            <h2>3. Rating Distribution by Genre</h2>
            <img src="/plots/rating_distribution_by_genre.png" onerror="this.parentElement.innerHTML='<p class=error>Plot failed to load</p>'">
        </div>
        <div class="plot">
            <h2>4. Average Rating: Genre × Region Heatmap</h2>
            <img src="/plots/heatmap_avg_rating.png" onerror="this.parentElement.innerHTML='<p class=error>Plot failed to load</p>'">
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/api/movies")
def api_movies():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, url, genres, region, rating FROM douban_top100_movies ORDER BY id;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{
            "id": r[0], "title": r[1], "url": r[2], 
            "genres": r[3], "region": r[4], "rating": float(r[5]) if r[5] else None
        } for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route("/plots/avg_rating_by_genre.png")
def plot1():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT genres, rating FROM douban_top100_movies WHERE genres IS NOT NULL AND rating IS NOT NULL", conn)
        conn.close()
        
        df["genres_en"] = df["genres"].apply(lambda x: translate_text(x, GENRE_MAP))
        df_ex = df.assign(genres_list=df["genres_en"].apply(split_genres)).explode("genres_list")
        df_ex = df_ex.drop(columns=["genres_en", "genres"])
        df_ex = df_ex.rename(columns={"genres_list": "genres_en"})
        df_ex = df_ex[df_ex["genres_en"] != ""].reset_index(drop=True)
        
        if len(df_ex) == 0:
            raise ValueError("No data after processing")
        
        avg = df_ex.groupby('genres_en')['rating'].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.bar(range(len(avg)), avg.values, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xticks(range(len(avg)))
        ax.set_xticklabels(avg.index, rotation=45, ha='right')
        ax.set_ylabel('Average Rating', fontsize=12)
        ax.set_xlabel('Genre', fontsize=12)
        ax.set_title('Average Rating by Genre', fontsize=14, fontweight='bold')
        ax.set_ylim(7, 10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        for i, (idx, val) in enumerate(avg.items()):
            ax.text(i, val + 0.05, f'{val:.2f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error in plot1: {e}")
        return f"Error generating plot: {str(e)}", 500

@app.route("/plots/movie_count_by_genre.png")
def plot2():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT genres FROM douban_top100_movies WHERE genres IS NOT NULL", conn)
        conn.close()
        
        df["genres_en"] = df["genres"].apply(lambda x: translate_text(x, GENRE_MAP))
        df_ex = df.assign(genres_list=df["genres_en"].apply(split_genres)).explode("genres_list")
        df_ex = df_ex.drop(columns=["genres_en", "genres"])
        df_ex = df_ex.rename(columns={"genres_list": "genres_en"})
        df_ex = df_ex[df_ex["genres_en"] != ""].reset_index(drop=True)
        
        if len(df_ex) == 0:
            raise ValueError("No data after processing")
        
        counts = df_ex['genres_en'].value_counts()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.bar(range(len(counts)), counts.values, color='coral', edgecolor='black', alpha=0.7)
        ax.set_xticks(range(len(counts)))
        ax.set_xticklabels(counts.index, rotation=45, ha='right')
        ax.set_ylabel('Number of Movies', fontsize=12)
        ax.set_xlabel('Genre', fontsize=12)
        ax.set_title('Number of Movies by Genre', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        for i, (idx, val) in enumerate(counts.items()):
            ax.text(i, val + 0.3, str(int(val)), ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error in plot2: {e}")
        return f"Error generating plot: {str(e)}", 500

@app.route("/plots/rating_distribution_by_genre.png")
def plot3():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT genres, rating FROM douban_top100_movies WHERE genres IS NOT NULL AND rating IS NOT NULL", conn)
        conn.close()
        
        df["genres_en"] = df["genres"].apply(lambda x: translate_text(x, GENRE_MAP))
        df_ex = df.assign(genres_list=df["genres_en"].apply(split_genres)).explode("genres_list")
        df_ex = df_ex.drop(columns=["genres_en", "genres"])
        df_ex = df_ex.rename(columns={"genres_list": "genres_en"})
        df_ex = df_ex[df_ex["genres_en"] != ""].reset_index(drop=True)
        
        if len(df_ex) == 0:
            raise ValueError("No data after processing")
        
        genre_order = df_ex['genres_en'].value_counts().index.tolist()
        
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.boxplot(data=df_ex, x='genres_en', y='rating', order=genre_order, 
                    hue='genres_en', palette='Set2', legend=False, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_ylabel('Rating', fontsize=12)
        ax.set_xlabel('Genre', fontsize=12)
        ax.set_title('Rating Distribution by Genre', fontsize=14, fontweight='bold')
        ax.set_ylim(6, 10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error in plot3: {e}")
        return f"Error generating plot: {str(e)}", 500

@app.route("/plots/heatmap_avg_rating.png")
def plot4():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT genres, region, rating FROM douban_top100_movies WHERE genres IS NOT NULL AND region IS NOT NULL AND rating IS NOT NULL", conn)
        conn.close()
        
        df["genres_en"] = df["genres"].apply(lambda x: translate_text(x, GENRE_MAP))
        df["region_en"] = df["region"].apply(lambda x: translate_text(x, REGION_MAP))
        
        df_ex = df.assign(genres_list=df["genres_en"].apply(split_genres)).explode("genres_list")
        df_ex = df_ex.drop(columns=["genres_en", "genres", "region"])
        df_ex = df_ex.rename(columns={"genres_list": "genres_en"})
        df_ex = df_ex[df_ex["genres_en"] != ""].reset_index(drop=True)
        
        pivot = df_ex.pivot_table(index='genres_en', columns='region_en', values='rating', aggfunc='mean')
        
        fig = plt.figure(figsize=(16, 10))
        sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Avg Rating'})
        plt.title('Average Rating by Genre and Region', fontsize=14, fontweight='bold')
        plt.ylabel('Genre', fontsize=12)
        plt.xlabel('Region', fontsize=12)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error in plot4: {e}")
        return f"Error generating plot: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
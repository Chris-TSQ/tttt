# 🎬 Douban Top 100 Movies Analysis

A full-stack data visualization project that analyzes the **Top 100 movies from Douban** using Python, Flask, Node.js, PostgreSQL/MySQL, and frontend interfaces (React + Vanilla JS).

This project provides:
- 📊 Dynamic data visualizations (genre, ratings, heatmaps)
- 🔌 RESTful APIs for movie data and statistics
- 🧠 Data cleaning & translation (Chinese → English)
- 🌐 Multiple frontends (React + static dashboard)

---

## 🚀 Features

### 📈 Data Analysis & Visualization
- Average rating by genre
- Movie count per genre
- Rating distribution (boxplots)
- Genre × Region heatmap

### 🔌 Backend APIs
- Fetch all movies
- Filter movies by genre
- Retrieve statistics (total movies, average rating, etc.)
- Health check endpoints

### 🧹 Data Processing
- Chinese → English translation for genres & regions
- Genre splitting and normalization
- Missing data handling

### 🎨 Frontend
- Interactive dashboard (Vanilla JS)
- React app for movie browsing
- Auto-refreshing visualizations

---

## 🏗️ Tech Stack

### Backend
- **Flask (Python)** – Data processing & plotting
- **Node.js (Express)** – API layer
- **MySQL / PostgreSQL** – Database
- **Pandas / Seaborn / Matplotlib** – Data analysis & visualization

### Frontend
- **React** – Movie list UI
- **Vanilla JavaScript** – Dashboard + stats
- **HTML/CSS** – UI layout

---

## 📁 Project Structure


project/
│
├── backend/
│ ├── app.py # Flask app (plots + API)
│ ├── plots/ # Generated plot images
│ └── .env # Environment variables
│
├── server/
│ └── index.js # Node.js Express API
│
├── frontend/
│ ├── App.js # React app
│ ├── api.js # API helper
│ ├── ui.js # UI utilities
│ └── config.js # Config settings
│
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/douban-movie-analysis.git
cd douban-movie-analysis
```
2️⃣ Backend (Flask)
Install dependencies
```
pip install flask flask-cors pandas matplotlib seaborn mysql-connector-python python-dotenv
Configure .env
DB_HOST=your_host
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
FLASK_DEBUG=False
Run Flask server
python app.py
```
Server runs on:

http://localhost:5000
3️⃣ Node.js API Server
Install dependencies
npm install express pg cors
Set environment variables
```
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=5432
Run server
node index.js
```
Server runs on:

http://localhost:10000
4️⃣ React Frontend
```
npm install
npm start
```
Runs on:

http://localhost:3000
📊 API Endpoints
Node.js API
Endpoint	Description
/api/health	Health check
/api/stats	Get statistics
/api/movies	Get all movies
/api/movies/genre/:genre	Filter by genre
/api/data	Top 100 dataset
Flask API
Endpoint	Description
/api/movies	Raw movie data
/plots/avg_rating_by_genre.png	Avg rating chart
/plots/movie_count_by_genre.png	Count chart
/plots/rating_distribution_by_genre.png	Boxplot
/plots/heatmap_avg_rating.png	Heatmap
## 📷 Visualizations
1. Average Rating by Genre
Bar chart
Shows highest-rated genres
2. Movie Count by Genre
Distribution of genres in dataset
3. Rating Distribution
Boxplot for rating spread
4. Heatmap (Genre × Region)
Cross-analysis of region and genre ratings
🔄 Data Processing Pipeline
Fetch raw data from database
Translate Chinese text → English
Split multi-genre strings
Normalize & clean data
Generate plots dynamically

## 🛠️ Improvements
 Unify database (choose PostgreSQL or MySQL)
 Add authentication
 Deploy with Docker
 Improve UI/UX
 Add caching for plots
 Fix API inconsistencies
🌐 Deployment

Example:

Backend: Render / Railway
Frontend: GitHub Pages / Vercel

## 📜 License

MIT License

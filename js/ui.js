class UI {
    static updateStats(movies) {
        const totalMovies = movies.length;
        const avgRating = (
            movies.reduce((sum, m) => sum + (m.rating || 0), 0) / totalMovies
        ).toFixed(2);
        
        const genres = new Set();
        movies.forEach(movie => {
            if (movie.genres) {
                movie.genres.split(/[/,]/).forEach(g => 
                    genres.add(g.trim())
                );
            }
        });

        document.getElementById('totalMovies').textContent = totalMovies;
        document.getElementById('avgRating').textContent = avgRating;
        document.getElementById('totalGenres').textContent = genres.size;
    }

    static showLoading() {
        document.querySelectorAll('.stat-value').forEach(el => {
            el.textContent = '...';
        });
    }

    static showError(message) {
        alert(`Error: ${message}`);
    }

    static showSuccess(message) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.cssText = 
            'position:fixed;top:20px;right:20px;background:#4caf50;' +
            'color:white;padding:15px 25px;border-radius:8px;' +
            'box-shadow:0 5px 15px rgba(0,0,0,0.3);z-index:1000';
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
}
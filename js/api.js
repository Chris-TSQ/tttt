class API {
    static async fetchMovies() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/stats`);
        throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    static getPlotUrl(plotName) {
        const timestamp = Date.now();
        return `${CONFIG.API_BASE_URL}${CONFIG.PLOTS_PATH}/${plotName}?v=${timestamp}`;
    }

    static async refreshPlots() {
        const images = document.querySelectorAll('.plot-card img');
        images.forEach(img => {
            const src = img.src.split('?')[0];
            img.src = `${src}?v=${Date.now()}`;
        });
    }
}
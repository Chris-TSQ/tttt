const CONFIG = {
  API_BASE_URL:
    // window.location.hostname === "localhost"
      // ? "http://localhost:5000"      : 
      "https://task3-xzjt.onrender.com",

  PLOT_MAPPINGS: {
    "avg-rating": "avg_rating_by_genre",
    "movie-count": "movie_count_by_genre",
    "rating-dist": "rating_distribution_by_genre",
    heatmap: "heatmap_avg_rating",
  },

  AUTO_REFRESH_INTERVAL: 300000,
  REQUEST_TIMEOUT: 10000,
};

const express = require("express");
const { Pool } = require("pg");
const cors = require("cors");
const path = require("path");

const app = express();

// CORS configuration
app.use(
  cors({
    origin: ["http://localhost:3000", "https://chris-tsq.github.io"],
    methods: ["GET", "POST"],
    credentials: true,
  })
);

app.use(express.json());

// PostgreSQL connection pool
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT || 5432,
  ssl: { rejectUnauthorized: false },
});

// Test database connection
pool.connect((err, client, release) => {
  if (err) {
    console.error("Error connecting to database:", err.stack);
  } else {
    console.log("✓ Database connected successfully");
    release();
  }
});

// Add this BEFORE your routes
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// Get statistics endpoint
app.get("/api/stats", async (req, res) => {
  try {
    const totalMoviesResult = await pool.query(
      "SELECT COUNT(*) as count FROM douban_movies_top"
    );

    const totalGenresResult = await pool.query(
      "SELECT COUNT(DISTINCT genre) as count FROM douban_movies_top"
    );

    const avgRatingResult = await pool.query(
      "SELECT AVG(rating) as avg_rating FROM douban_movies_top"
    );

    const highestRatedResult = await pool.query(
      "SELECT title FROM douban_movies_top ORDER BY rating DESC LIMIT 1"
    );

    const stats = {
      total_movies: parseInt(totalMoviesResult.rows[0].count),
      total_genres: parseInt(totalGenresResult.rows[0].count),
      avg_rating: parseFloat(avgRatingResult.rows[0].avg_rating),
      highest_rated: highestRatedResult.rows[0]?.title || "N/A",
    };

    res.json(stats);
  } catch (err) {
    console.error("Error fetching stats:", err);
    res.status(500).json({ error: "Failed to fetch statistics" });
  }
});

// Get all movies endpoint
app.get("/api/movies", async (req, res) => {
  try {
    const result = await pool.query(
      "SELECT * FROM douban_movies_top ORDER BY rating DESC"
    );
    res.json(result.rows);
  } catch (err) {
    console.error("Error fetching movies:", err);
    res.status(500).json({ error: "Failed to fetch movies" });
  }
});

// Get movies by genre
app.get("/api/movies/genre/:genre", async (req, res) => {
  try {
    const { genre } = req.params;
    const result = await pool.query(
      "SELECT * FROM douban_movies_top WHERE genre ILIKE $1 ORDER BY rating DESC",
      [`%${genre}%`]
    );
    res.json(result.rows);
  } catch (err) {
    console.error("Error fetching movies by genre:", err);
    res.status(500).json({ error: "Failed to fetch movies by genre" });
  }
});

// Add this route if you need /api/data endpoint
app.get("/api/data", async (req, res) => {
  try {
    const result = await pool.query(
      "SELECT * FROM douban_movies_top ORDER BY rating DESC LIMIT 100"
    );
    res.json(result.rows);
  } catch (err) {
    console.error("Error fetching data:", err);
    res.status(500).json({ error: "Failed to fetch data" });
  }
});

// Serve static plot images
app.use("/plots", express.static(path.join(__dirname, "plots")));

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: "Endpoint not found" });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Server error:", err.stack);
  res.status(500).json({ error: "Internal server error" });
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`\n🚀 Server running on port ${PORT}`);
  console.log(`📊 API endpoints:`);
  console.log(`   GET  /api/health`);
  console.log(`   GET  /api/stats`);
  console.log(`   GET  /api/movies`);
  console.log(`   GET  /api/movies/genre/:genre`);
  console.log(`   GET  /plots/:filename.png\n`);
});

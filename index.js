const express = require("express");
const { Pool } = require("pg");
const cors = require("cors");
app.use(cors({ origin: "https://your-frontend-domain.github.io" }));

const app = express();
app.use(cors()); // Allow cross-origin requests from your frontend domain

const pool = new Pool({
  user: "YOUR_AIVEN_DB_USER",
  host: "YOUR_AIVEN_HOST",
  database: "YOUR_DB_NAME",
  password: "YOUR_AIVEN_PASSWORD",
  port: 5432,
  ssl: { rejectUnauthorized: false }, // often needed with cloud DBs
});

app.get("/api/data", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM your_table");
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

// in frontend code
fetch("https://your-backend.onrender.com/api/data")
  .then((r) => r.json())
  .then((data) => {
    /* draw charts */
  });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API server is running on port ${PORT}`));

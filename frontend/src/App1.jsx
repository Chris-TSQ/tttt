import React, { useEffect, useState } from "react";

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/movies")
      .then(res => res.json())
      .then(data => setMovies(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>My Movie Visualizations</h1>

      {/* Show movie list */}
      <ul>
        {movies.map((m, i) => (
          <li key={i}>{m.rank} — {m.title}</li>
        ))}
      </ul>

      {/* Show plots */}
      <h2>Plots</h2>
      <img src="http://localhost:5000/plots/heatmap.png" alt="Heatmap" style={{maxWidth:"100%"}} />
      <img src="http://localhost:5000/plots/barplot1.png" alt="Barplot" style={{maxWidth:"100%"}} />
      {/* etc */}
    </div>
  );
}

export default App;

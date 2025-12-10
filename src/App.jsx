import React, {useState, useEffect} from 'react';

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/movies")
      .then(r => r.json())
      .then(setMovies)
      .catch(console.error);
  }, []);

  return (
    <div style={{padding: '20px'}}>
      <h1>Movie List</h1>

      <ul>
        {movies.map(m => (
          <li key={m.id}>  {/* Use m.id instead of m.rank */}
            {m.title} — {m.region} — Rating: {m.rating}
          </li>
        ))}
      </ul>

      <h2>Plots</h2>
      <img src="http://localhost:5000/plots/movies_by_genre.png" style={{maxWidth: "800px"}}/>
      <img src="http://localhost:5000/plots/avg_rating_by_genre.png" style={{maxWidth: "800px"}}/>
      <img src="http://localhost:5000/plots/heatmap_avg_rating.png" style={{maxWidth: "800px"}}/>
    </div>
  );
}

export default App;

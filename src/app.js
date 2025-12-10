export async function fetchMovies(){
	const res = await fetch('/api/movies');
	return res.json();
}


export function mountPlots(){
	const plots = [
		'/plots/avg_rating_by_genre.png',
		'/plots/movie_count_by_genre.png',
		'/plots/rating_distribution_by_genre.png',
		'/plots/heatmap_avg_rating.png'
	];
	const container = document.getElementById('plots');
	plots.forEach(p=>{
		const img = document.createElement('img'); img.src=p; img.style.width='100%'; img.style.maxWidth='900px';
		container.appendChild(img);
	});
}
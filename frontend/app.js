const API_URL = "http://localhost:5000/movies"; // CHANGE after deploy
const PAGE_SIZE = 10;

let movies = [];
let currentPage = 1;

// ---------- READ ----------
async function loadMovies() {
    const res = await fetch(API_URL);
    movies = await res.json();
    renderMovies();
}

// ---------- CREATE / UPDATE ----------
document.getElementById("movieForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = movieId.value;
    const movie = {
        title: title.value,
        genre: genre.value,
        year: Number(year.value),
        rating: Number(rating.value)
    };

    if (id) {
        // UPDATE
        await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(movie)
        });
    } else {
        // CREATE
        await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(movie)
        });
    }

    e.target.reset();
    movieId.value = "";
    loadMovies();
});

// ---------- DELETE ----------
async function deleteMovie(id) {
    if (!confirm("Are you sure you want to delete this movie?")) return;

    await fetch(`${API_URL}/${id}`, { method: "DELETE" });

    // Handle page overflow after delete
    if ((currentPage - 1) * PAGE_SIZE >= movies.length - 1) {
        currentPage = Math.max(1, currentPage - 1);
    }

    loadMovies();
}

// ---------- EDIT ----------
function editMovie(id) {
    const movie = movies.find(m => m.id === id);

    movieId.value = movie.id;
    title.value = movie.title;
    genre.value = movie.genre;
    year.value = movie.year;
    rating.value = movie.rating;
}

// ---------- RENDER + PAGING ----------
function renderMovies() {
    const table = document.getElementById("movieTable");
    table.innerHTML = "";

    const start = (currentPage - 1) * PAGE_SIZE;
    const pageMovies = movies.slice(start, start + PAGE_SIZE);

    pageMovies.forEach(movie => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${movie.title}</td>
            <td>${movie.genre}</td>
            <td>${movie.year}</td>
            <td>${movie.rating}</td>
            <td>
                <button onclick="editMovie(${movie.id})">Edit</button>
                <button onclick="deleteMovie(${movie.id})">Delete</button>
            </td>
        `;
        table.appendChild(row);
    });

    pageNum.textContent = `Page ${currentPage}`;
    updateStats();
}

// ---------- PAGING BUTTONS ----------
function nextPage() {
    if (currentPage * PAGE_SIZE < movies.length) {
        currentPage++;
        renderMovies();
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderMovies();
    }
}

// ---------- STATS ----------
function updateStats() {
    totalMovies.textContent = movies.length;

    const avg =
        movies.reduce((sum, m) => sum + m.rating, 0) / movies.length;

    avgRating.textContent = avg.toFixed(1);
}

// ---------- INIT ----------
loadMovies();

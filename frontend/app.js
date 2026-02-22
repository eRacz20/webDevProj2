const API_URL = "http://localhost:5000/movies";
const PAGE_SIZE = 10;

let movies = [];
let currentPage = 1;

// ---------- LOAD ----------
async function loadMovies() {
    const res = await fetch(API_URL);
    movies = await res.json();
    populateGenres();
    renderMovies();
}

// ---------- FORM ----------
document.getElementById("movieForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = movieId.value;

    const movie = {
        title: title.value,
        genre: genre.value,
        year: Number(year.value),
        rating: Number(rating.value),
        image_url: image_url.value
    };

    if (id) {
        await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(movie)
        });
    } else {
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
    if (!confirm("Delete this movie?")) return;
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
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
    image_url.value = movie.image_url || "";
}

// ---------- GENRE LIST ----------
function populateGenres() {
    const genres = [...new Set(movies.map(m => m.genre))];
    genreFilter.innerHTML =
        `<option value="">All Genres</option>` +
        genres.map(g => `<option>${g}</option>`).join("");
}

// ---------- FILTER ----------
function getFilteredMovies() {
    let filtered = [...movies];

    if (searchBox.value)
        filtered = filtered.filter(m =>
            m.title.toLowerCase().includes(searchBox.value.toLowerCase())
        );

    if (genreFilter.value)
        filtered = filtered.filter(m => m.genre === genreFilter.value);

    if (sortBy.value)
        filtered.sort((a, b) =>
            typeof a[sortBy.value] === "string"
                ? a[sortBy.value].localeCompare(b[sortBy.value])
                : b[sortBy.value] - a[sortBy.value]
        );

    return filtered;
}

// ---------- RENDER ----------
function renderMovies() {
    const table = movieTable;
    table.innerHTML = "";

    const filtered = getFilteredMovies();

    const start = (currentPage - 1) * PAGE_SIZE;
    const pageMovies = filtered.slice(start, start + PAGE_SIZE);

    pageMovies.forEach(movie => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>
                <img src="${movie.image_url || 'https://via.placeholder.com/80'}"
                onerror="this.src='https://via.placeholder.com/80'" width="60">
            </td>
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
    totalMovies.textContent = filtered.length;
}

// ---------- PAGING ----------
function nextPage() {
    currentPage++;
    renderMovies();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderMovies();
    }
}

// ---------- EVENTS ----------
searchBox.oninput = () => { currentPage = 1; renderMovies(); };
genreFilter.onchange = () => { currentPage = 1; renderMovies(); };
sortBy.onchange = () => { currentPage = 1; renderMovies(); };

// ---------- INIT ----------
loadMovies();
const API_URL = "https://webdevproj2.onrender.com/movies";

let movies = [];
let currentPage = 1;
let PAGE_SIZE = 10;

// ---------- COOKIE ----------
function setCookie(name, value) {
    document.cookie = `${name}=${value};path=/;max-age=31536000`;
}

function getCookie(name) {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith(name + "="))
        ?.split("=")[1];
}

// ---------- LOAD ----------
async function loadMovies() {
    const res = await fetch(API_URL);
    movies = await res.json();

    const saved = getCookie("pageSize");
    if (saved) {
        PAGE_SIZE = Number(saved);
        pageSizeSelect.value = saved;
    }

    populateGenres();
    renderMovies();
}

// ---------- FORM ----------
movieForm.addEventListener("submit", async e => {
    e.preventDefault();

    const movie = {
        title: title.value,
        genre: genre.value,
        year: Number(year.value),
        rating: Number(rating.value),   // ⭐ ensure number
        image_url: image_url.value
    };

    if (movieId.value)
        await fetch(`${API_URL}/${movieId.value}`, {
            method: "PUT",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(movie)
        });
    else
        await fetch(API_URL, {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(movie)
        });

    movieForm.reset();
    movieId.value = "";
    loadMovies();
});

// ---------- EDIT ----------
function editMovie(id) {
    const m = movies.find(x => x.id === id);
    movieId.value = m.id;
    title.value = m.title;
    genre.value = m.genre;
    year.value = m.year;
    rating.value = m.rating;
    image_url.value = m.image_url || "";
}

// ---------- DELETE ----------
async function deleteMovie(id) {
    if (!confirm("Delete this movie?")) return;
    await fetch(`${API_URL}/${id}`, {method:"DELETE"});
    loadMovies();
}

// ---------- FILTER ----------
function getFiltered() {
    let list = [...movies];

    if (searchBox.value)
        list = list.filter(m =>
            m.title.toLowerCase().includes(searchBox.value.toLowerCase())
        );

    if (genreFilter.value)
        list = list.filter(m => m.genre === genreFilter.value);

    if (sortBy.value)
        list.sort((a,b)=>
            typeof a[sortBy.value] === "string"
                ? a[sortBy.value].localeCompare(b[sortBy.value])
                : b[sortBy.value]-a[sortBy.value]
        );

    return list;
}

// ---------- RENDER ----------
function renderMovies() {
    movieTable.innerHTML = "";

    const filtered = getFiltered();

    const start = (currentPage-1)*PAGE_SIZE;
    const page = filtered.slice(start,start+PAGE_SIZE);

    page.forEach(m=>{
        movieTable.innerHTML += `
        <tr>
            <td>
                <img src="${m.image_url || 'https://via.placeholder.com/80'}"
                onerror="this.src='https://via.placeholder.com/80'"
                width="60">
            </td>
            <td>${m.title}</td>
            <td>${m.genre}</td>
            <td>${m.year}</td>
            <td>${m.rating}</td>
            <td>
                <button onclick="editMovie(${m.id})">Edit</button>
                <button onclick="deleteMovie(${m.id})">Delete</button>
            </td>
        </tr>`;
    });

    pageNum.textContent = `Page ${currentPage}`;

    // ⭐ FIX — UPDATE STATS HERE
    updateStats(filtered);
}

// ---------- STATS ----------
function updateStats(filtered) {
    totalMovies.textContent = filtered.length;
    currentPageSize.textContent = PAGE_SIZE;

    if (filtered.length === 0) {
        avgRating.textContent = 0;
        return;
    }

    const avg =
        filtered.reduce((sum, m) => sum + Number(m.rating || 0), 0)
        / filtered.length;

    avgRating.textContent = avg.toFixed(1);
}

// ---------- GENRES ----------
function populateGenres(){
    const genres=[...new Set(movies.map(m=>m.genre))];
    genreFilter.innerHTML="<option value=''>All Genres</option>"
        +genres.map(g=>`<option>${g}</option>`).join("");
}

// ---------- PAGING ----------
function nextPage(){
    currentPage++;
    renderMovies();
}

function prevPage(){
    if(currentPage>1){currentPage--;renderMovies();}
}

// ---------- EVENTS ----------
searchBox.oninput=()=>{currentPage=1;renderMovies();}
genreFilter.onchange=()=>{currentPage=1;renderMovies();}
sortBy.onchange=()=>{currentPage=1;renderMovies();}

pageSizeSelect.onchange=()=>{
    PAGE_SIZE=Number(pageSizeSelect.value);
    setCookie("pageSize",PAGE_SIZE);
    currentPage=1;
    renderMovies();
}

// ---------- INIT ----------
loadMovies();
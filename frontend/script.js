const API="ttps://webdevproj2.onrender.com";

let page=1;
let size=localStorage.getItem("size")||10;
document.getElementById("size").value=size;

function imgError(img){
    img.src="placeholder.png";
}

async function load(){
    size=document.getElementById("size").value;
    localStorage.setItem("size",size);

    let search=document.getElementById("search").value;
    let sort=document.getElementById("sort").value;

    let r=await fetch(`${API}/movies?page=${page}&size=${size}&search=${search}&sort=${sort}`);
    let j=await r.json();

    document.getElementById("page").innerText=`Page ${page}`;

    let html="";
    j.movies.forEach(m=>{
        html+=`
        <div class="card">
            <img src="${m.image_url}" onerror="imgError(this)">
            <div>
                <b>${m.title}</b> (${m.year})<br>
                ${m.genre} ⭐${m.rating}<br>
                <button onclick="del(${m.id})">Delete</button>
            </div>
        </div>`;
    });

    document.getElementById("movies").innerHTML=html;

    let s=await fetch(`${API}/stats`);
    let stats=await s.json();
    document.getElementById("stats").innerHTML=
        `Total Movies: ${stats.total}<br>
         Avg Rating: ${Number(stats.avg_rating).toFixed(2)}<br>
         Genres: ${stats.genres}`;
}

async function del(id){
    if(!confirm("Delete movie?")) return;
    await fetch(`${API}/movies/${id}`,{method:"DELETE"});
    load();
}

function next(){page++;load();}
function prev(){if(page>1)page--;load();}

load();
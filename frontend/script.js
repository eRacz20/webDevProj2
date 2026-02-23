const API="https://webdevproj2.onrender.com";

let page=1;
let editing=null;

document.getElementById("size").value=
localStorage.getItem("size")||10;

function imgError(img){
 img.src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Film_reel_icon.svg/512px-Film_reel_icon.svg.png";
}

async function load(){

 let size=document.getElementById("size").value;
 localStorage.setItem("size",size);

 let search=document.getElementById("search").value;
 let rating=document.getElementById("ratingFilter").value;
 let sort=document.getElementById("sort").value;

 let r=await fetch(`${API}/movies?page=${page}&size=${size}&search=${search}&rating=${rating}&sort=${sort}`);
 let j=await r.json();

 document.getElementById("pageNum").innerText=`Page ${page}`;

 let html="";
 j.movies.forEach(m=>{
  html+=`
  <div class="card">
   <img src="${m.image_url}" onerror="imgError(this)">
   <h3>${m.title} (${m.year})</h3>
   <p>${m.genre} ⭐${m.rating}</p>
   <button onclick="edit(${m.id})">Edit</button>
   <button onclick="del(${m.id})">Delete</button>
  </div>`;
 });

 document.getElementById("movies").innerHTML=html;

 let s=await fetch(`${API}/stats`);
 let stats=await s.json();
 document.getElementById("stats").innerHTML=
 `Total Movies: ${stats.total} | Avg Rating: ${Number(stats.avg_rating).toFixed(2)}`;
}

function next(){page++;load();}
function prev(){if(page>1)page--;load();}

async function add(){

 let data={
  title:title.value,
  year:year.value,
  genre:genre.value,
  rating:rating.value,
  image_url:image.value
 };

 if(editing){
  await fetch(`${API}/movies/${editing}`,{
   method:"PUT",
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify(data)
  });
  editing=null;
 }else{
  await fetch(`${API}/movies`,{
   method:"POST",
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify(data)
  });
 }

 load();
}

async function edit(id){
 let r=await fetch(`${API}/movies`);
 let j=await r.json();
 let m=j.movies.find(x=>x.id===id);

 title.value=m.title;
 year.value=m.year;
 genre.value=m.genre;
 rating.value=m.rating;
 image.value=m.image_url;

 editing=id;
}

async function del(id){
 if(!confirm("Delete movie?")) return;
 await fetch(`${API}/movies/${id}`,{method:"DELETE"});
 load();
}

load();
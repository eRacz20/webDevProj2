const API="https://webdevproj2.onrender.com";
let editId=null;

async function loadMovies(){
 let search=document.getElementById("search").value;
 let rating=document.getElementById("ratingFilter").value;

 let res=await fetch(`${API}/movies?search=${search}&rating=${rating}`);
 let data=await res.json();

 let html="";
 data.movies.forEach(m=>{
 html+=`
 <div class="card">
 <img src="${m.image_url}" onerror="this.src='https://via.placeholder.com/120x180'"><br>
 <b>${m.title}</b> (${m.year})<br>
 ${m.genre} ⭐${m.rating}<br>
 <button onclick="startEdit(${m.id},'${m.title}',${m.year},'${m.genre}',${m.rating},'${m.image_url}')">Edit</button>
 <button onclick="del(${m.id})">Delete</button>
 </div>`;
 });

 document.getElementById("movies").innerHTML=html;

 let st=await fetch(`${API}/stats`);
 let stats=await st.json();
 document.getElementById("stats").innerHTML=
 `Total Movies: ${stats.total} | Avg Rating: ${stats.avg_rating}`;
}

function startEdit(id,t,y,g,r,i){
 editId=id;
 title.value=t;
 year.value=y;
 genre.value=g;
 rating.value=r;
 image.value=i;
}

async function saveMovie(){
 let data={
  title:title.value,
  year:parseInt(year.value),
  genre:genre.value,
  rating:parseInt(rating.value),
  image_url:image.value
 };

 if(editId){
  await fetch(`${API}/movies/${editId}`,{
   method:"PUT",
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify(data)
  });
  editId=null;
 }else{
  await fetch(`${API}/movies`,{
   method:"POST",
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify(data)
  });
 }

 loadMovies();
}

async function del(id){
 if(!confirm("Delete movie?")) return;
 await fetch(`${API}/movies/${id}`,{method:"DELETE"});
 loadMovies();
}

loadMovies();
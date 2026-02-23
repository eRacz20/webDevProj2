# DEPLOYMENT.md

## Project Name

Production Collection Manager – Movie Collection App

---

## 1. Domain Information

* **Domain Name:** yourdomain.com
* **Registrar:** (Namecheap, GoDaddy, Google Domains, etc.)
* **HTTPS Enabled:** Yes (via hosting provider SSL certificate)

---

## 2. Hosting Providers

* **Frontend Hosting:** Netlify
* **Backend Hosting:** Render
* **Database Hosting:** Render PostgreSQL

All services are publicly accessible and connected through HTTPS.

---

## 3. Technology Stack

* **Frontend:** HTML + CSS + JavaScript (or React if used)
* **Backend:** Python Flask API
* **Database:** PostgreSQL
* **Image Source:** Movie poster URLs from TMDB image links

---

## 4. Database Setup

* Database Type: PostgreSQL
* Hosted on: Render PostgreSQL instance
* Tables Created Automatically on Startup using `init_db()` in `app.py`
* Seed Data: 30+ movies inserted automatically if database is empty

Schema Example:

```
movies(
  id SERIAL PRIMARY KEY,
  title TEXT,
  year INT,
  genre TEXT,
  rating INT,
  image_url TEXT
)
```

---

## 5. Environment Variables / Secrets

Secrets are NOT stored in GitHub.

Environment variables are configured in Render dashboard:

```
DATABASE_URL=postgresql://username:password@host:port/dbname
PORT=10000
```

These are accessed in Flask using:

```
os.getenv("DATABASE_URL")
```

---

## 6. How to Deploy the Application

### Backend (Render)

1. Push backend code to GitHub.
2. Connect GitHub repo to Render.
3. Set Build Command:

   ```
   pip install -r requirements.txt
   ```
4. Set Start Command:

   ```
   gunicorn app:app
   ```
5. Add environment variable DATABASE_URL.
6. Deploy service.

### Frontend (Netlify)

1. Push frontend code to GitHub.
2. Connect repo to Netlify.
3. Set build settings (if React):

   ```
   npm run build
   ```
4. Set publish folder (build or root folder).
5. Deploy site.

### Custom Domain Setup

1. Purchase domain from registrar.
2. Add domain to Netlify.
3. Update DNS records to point to Netlify.
4. Enable HTTPS certificate.

---

## 7. Updating the App

To update the app:

1. Make code changes locally.
2. Push to GitHub.
3. Render and Netlify automatically redeploy.

No manual server setup required.

---

## 8. Application Features

The deployed app includes:

* Full CRUD operations using SQL database
* 30+ seeded movie records
* Image thumbnails for each record
* Search and filtering by title/rating
* Sorting by title, year, or rating
* Paging with user‑selected page size stored in cookies
* Stats page showing total records and average rating
* Delete confirmation before removing a movie
* Responsive UI for desktop and mobile

---

## 9. Live Links

* **Live Website:** [https://yourdomain.com](https://yourdomain.com)
* **GitHub Repo:** [https://github.com/yourusername/yourrepo](https://github.com/yourusername/yourrepo)
* **Backend API:** [https://yourbackend.onrender.com](https://yourbackend.onrender.com)

---

## 10. Notes for Instructor

The application is fully public and requires no login.
All database operations persist correctly, and the app can be tested directly through the live site.

---

If you have any trouble accessing the app, please contact me and I will respond quickly.

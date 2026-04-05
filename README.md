# 🎬 Videoflix Backend

Django REST API for a Netflix-style video streaming platform.

🌍 Live version:  
🔗 [https://tim-thiele.de](https://tim-thiele.de)

---

## 🚀 Features

- 👤 User registration, login, logout
- 🔐 JWT authentication via HTTPOnly cookies
- 📧 Email verification & password reset
- 🎥 HLS video streaming (.m3u8 & .ts)
- ⚙️ Background tasks with Redis & Django-RQ
- 🐳 PostgreSQL, Redis & Backend via Docker

---

## 📋 Prerequisites

- 🐳 Docker & Docker Desktop (Recommended for all platforms)
- 🐍 Python 3.x & FFmpeg (Only needed for Local Installation)

---

## 🐳 Docker Installation (Recommended - Mac/Linux/Windows)

The easiest way to run the entire backend (Database, Redis, Worker, and Django API) locally without installing dependencies natively.

### 1. Clone Repository
```bash
git clone https://github.com/Greedrache/Videoflix .
```

### 2. Configure Environment Variables (.env)

Create a `.env` file in the root directory (where `docker-compose.yml` is) and add:
```env
SECRET_KEY=your_secure_key
DJANGO_DEBUG=True
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 3. Start everything with Docker

This command builds the backend container, installs all Python requirements, creates the database, runs migrations, and starts the Django server alongside Redis and PostgreSQL.
```bash
docker-compose up --build
```

🌐 Running on: http://127.0.0.1:8000  
(No need to run `manage.py runserver` or `rqworker` manually, Docker does everything!)

---

## 💻 Local Installation (Alternative - Windows mostly)

Only use this if you do not want to use the full Docker setup.

### 1. Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/Greedrache/Videoflix .
python -m venv venv
```

Windows:
```bash
.\venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Docker (Database + Redis ONLY)
```bash
docker-compose up db redis -d
```

### 4. Set Up Database Locally
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Running the Project Locally

Terminal 1 – Django Server:
```bash
python manage.py runserver
```

Terminal 2 – Background Worker (Video Conversion):
```bash
python manage.py rqworker default
```

---

## 🔌 API Endpoints

### 🔐 Authentication

| Method | Endpoint |
|--------|----------|
| POST | `/api/register/` |
| GET | `/api/activate/<uidb64>/<token>/` |
| POST | `/api/login/` |
| POST | `/api/logout/` |
| POST | `/api/token/refresh/` |
| POST | `/api/password_reset/` |
| POST | `/api/password_confirm/<uidb64>/<token>/` |

### 🎬 Videos

| Method | Endpoint |
|--------|----------|
| GET | `/api/video/` |
| GET | `/api/video/<id>/<resolution>/index.m3u8` |
| GET | `/api/video/<id>/<resolution>/<segment>` |

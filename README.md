# Videoflix Backend

Welcome to the backend of the **Videoflix** project! This is a Django REST API for a video streaming platform (similar to Netflix). It provides user authentication (JWT in HTTPOnly cookies), email verification, password reset, and dynamic **HLS video streaming**.

## 🚀 Features

*   **User Management:** Registration, Login, Logout, Email Verification, and Password Reset.
*   **Secure Authentication:** Tokens are securely exchanged via HTTPOnly cookies.
*   **Video Streaming:** Conversion of uploaded videos (.mp4) to HLS format (.m3u8 & .ts segments) using FFmpeg for smooth streaming.
*   **Background Tasks:** Video conversion via Redis and Django-RQ (Task Queues).
*   **Database:** PostgreSQL database (containerized via Docker).

---

## 🛠️ Prerequisites

Before you start, make sure the following are installed on your system:
1.  **Python 3.x** (incl. pip)
2.  **Docker & Docker Desktop** (to run the PostgreSQL database and Redis)
3.  **FFmpeg** (For video conversion - must be added to the Windows environment variables PATH)

---

## ⚙️ Installation & Setup

### 1. Setup Environment
Create a python virtual environment and activate it:
\\ash
python -m venv venv
.\venv\Scripts\activate   # On Windows
\
Install all required dependencies:
\\ash
pip install -r requirements.txt
\
### 2. Start Docker & Database
Start the database (PostgreSQL) and Redis using Docker Compose:
\\ash
docker-compose up -d
\
### 3. Environment Variables (.env)
Create a \.env\ file in the root directory (if not exists) and add your credentials:
\\ini
SECRET_KEY=your_secure_django_key
DJANGO_DEBUG=True
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_URL=redis://localhost:6379/1

# Email SMTP (For Registration Emails / Password Reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_google_app_password
\
### 4. Database Setup (Migrations)
Run the Django database migrations:
\\ash
python manage.py makemigrations
python manage.py migrate
\
Optional: Create an admin user for the Django backend (\/admin/\):
\\ash
python manage.py createsuperuser
\
---

## 🖥️ Running the Project

To run the project locally, you need **two** open terminals:

**Terminal 1: The Django Webserver**
\\ash
python manage.py runserver
\The server is now running at \http://127.0.0.1:8000/\.

**Terminal 2: The Background Worker (Video Conversion)**
*(Note: The virtual environment must be activated here too!)*
\\ash
python manage.py rqworker default
\This worker converts newly uploaded videos into the streaming format in the background.

---

## 📡 API Endpoints (Overview)

**User Auth:**
*   \POST /api/register/\ - Create account (sends email)
*   \GET /api/activate/<uidb64>/<token>/\ - Activate account
*   \POST /api/login/\ - Login (sets secure JWT cookies)
*   \POST /api/logout/\ - Logout (deletes cookies & blacklists token)
*   \POST /api/token/refresh/\ - Request a new Access Token
*   \POST /api/password_reset/\ - Reset password (sends email link)
*   \POST /api/password_confirm/<uidb64>/<token>/\ - Set new password

**Videos (Content):**
*   \GET /api/video/\ - Returns the list of all videos (Protected via JWT)
*   \GET /api/video/<movie_id>/<resolution>/index.m3u8\ - Loads the playlist for the video player
*   \GET /api/video/<movie_id>/<resolution>/<segment>\ - Loads the actual video chunks (.ts)

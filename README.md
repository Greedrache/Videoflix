<h1>🎬 Videoflix Backend</h1>

<p>Django REST API for a Netflix-style video streaming platform.</p>

<p>🌍 Live version:<br>
🔗 <a href="https://tim-thiele.de" target="_blank">https://tim-thiele.de</a></p>

<hr>

<h2>🚀 Features</h2>
<ul>
<li>👤 User registration, login, logout</li>
<li>🔐 JWT authentication via HTTPOnly cookies</li>
<li>📧 Email verification & password reset</li>
<li>🎥 HLS video streaming (.m3u8 & .ts)</li>
<li>⚙️ Background tasks with Redis & Django-RQ</li>
<li>🐳 PostgreSQL, Redis & Backend via Docker</li>
</ul>

<hr>

<h2>📋 Prerequisites</h2>
<ul>
<li>🐳 Docker & Docker Desktop (Recommended for all platforms)</li>
<li>🐍 Python 3.x & FFmpeg (Only needed for Local Installation)</li>
</ul>

<hr>

<h2>🐳 Docker Installation (Recommended - Mac/Linux/Windows)</h2>

<p>The easiest way to run the entire backend (Database, Redis, Worker, and Django API) locally without installing dependencies natively.</p>

<h3>1. Clone Repository</h3>
<pre><code>git clone https://github.com/Greedrache/Vdeoflix .</code></pre>

<h3>2. Configure Environment Variables (.env)</h3>
<p>Create a <code>.env</code> file in the root directory (where <code>docker-compose.yml</code> is) and add:</p>

<pre><code>SECRET_KEY=your_secure_key
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
</code></pre>

<h3>3. Start everything with Docker</h3>
<p>This command builds the backend container, installs all Python requirements, creates the database, runs migrations, and starts the Django server alongside Redis and PostgreSQL.</p>

<pre><code>docker-compose up --build</code></pre>

<p>🌐 Running on: http://127.0.0.1:8000 (No need to run <code>manage.py runserver</code> or <code>rqworker</code> manually, Docker does everything!)</p>

<hr>

<h2>💻 Local Installation (Alternative - Windows mostly)</h2>

<p>Only use this if you do not want to use the full Docker setup.</p>

<h3>1. Clone Repository & Create Virtual Environment</h3>
<pre><code>git clone https://github.com/Greedrache/Vdeoflix .
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
</code></pre>

<h3>2. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>3. Start Docker (Database + Redis ONLY)</h3>
<pre><code>docker-compose up db redis -d</code></pre>

<h3>4. Set Up Database Locally</h3>
<pre><code>python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
</code></pre>

<h3>5. Running the Project Locally</h3>

<p>Terminal 1: Django Server</p>
<pre><code>python manage.py runserver</code></pre>

<p>Terminal 2: Background Worker (Video Conversion)</p>
<pre><code>python manage.py rqworker default</code></pre>

<hr>

<h2>🔌 API Endpoints</h2>

<h3>🔐 Authentication</h3>
<ul>
<li>POST /api/register/</li>
<li>GET /api/activate/&lt;uidb64&gt;/&lt;token&gt;/</li>
<li>POST /api/login/</li>
<li>POST /api/logout/</li>
<li>POST /api/token/refresh/</li>
<li>POST /api/password_reset/</li>
<li>POST /api/password_confirm/&lt;uidb64&gt;/&lt;token&gt;/</li>
</ul>

<h3>🎬 Videos</h3>
<ul>
<li>GET /api/video/</li>
<li>GET /api/video/&lt;id&gt;/&lt;resolution&gt;/index.m3u8</li>
<li>GET /api/video/&lt;id&gt;/&lt;resolution&gt;/&lt;segment&gt;</li>
</ul>

<h1>🎬 Videoflix Backend</h1>

<p>
Django REST API for a video streaming platform (Netflix-style).
</p>

<p>
🌍 Live version:<br>
👉 <a href="https://tim-thiele.de" target="_blank">https://tim-thiele.de</a>
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
<li>👤 User registration, login, logout</li>
<li>🔐 JWT authentication via HTTPOnly cookies</li>
<li>📧 Email verification & password reset</li>
<li>🎥 HLS video streaming (.m3u8 & .ts)</li>
<li>⚡ Background tasks with Redis & Django-RQ</li>
<li>🐳 PostgreSQL via Docker</li>
</ul>

<hr>

<h2>🛠️ Prerequisites</h2>

<ul>
<li>Python 3.x</li>
<li>Docker & Docker Desktop</li>
<li>FFmpeg (must be added to PATH)</li>
</ul>

<hr>

<h2>⚙️ Installation</h2>

<h3>1. Create Virtual Environment</h3>

<pre><code id="venv">
python -m venv venv
.\venv\Scripts\activate
</code></pre>
<button onclick="copy('venv')">Copy</button>

<h3>2. Install Dependencies</h3>

<pre><code id="pip">
pip install -r requirements.txt
</code></pre>
<button onclick="copy('pip')">Copy</button>

<h3>3. Start Docker (Database + Redis)</h3>

<pre><code id="docker">
docker-compose up -d
</code></pre>
<button onclick="copy('docker')">Copy</button>

<hr>

<h2>🔐 Environment Variables (.env)</h2>

<pre><code id="env">
SECRET_KEY=your_secure_key
DJANGO_DEBUG=True

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_URL=redis://localhost:6379/1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
</code></pre>
<button onclick="copy('env')">Copy</button>

<hr>

<h2>🗄️ Database Setup</h2>

<pre><code id="migrate">
python manage.py makemigrations
python manage.py migrate
</code></pre>
<button onclick="copy('migrate')">Copy</button>

<h3>Optional: Create Admin User</h3>

<pre><code id="admin">
python manage.py createsuperuser
</code></pre>
<button onclick="copy('admin')">Copy</button>

<hr>

<h2>▶️ Running the Project</h2>

<h3>Terminal 1: Django Server</h3>

<pre><code id="run">
python manage.py runserver
</code></pre>
<button onclick="copy('run')">Copy</button>

<p>👉 Running on: http://127.0.0.1:8000</p>

<h3>Terminal 2: Background Worker (Video Conversion)</h3>

<pre><code id="worker">
python manage.py rqworker default
</code></pre>
<button onclick="copy('worker')">Copy</button>

<hr>

<h2>📡 API Endpoints</h2>

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

<h3>🎥 Videos</h3>

<ul>
<li>GET /api/video/</li>
<li>GET /api/video/&lt;id&gt;/&lt;resolution&gt;/index.m3u8</li>
<li>GET /api/video/&lt;id&gt;/&lt;resolution&gt;/&lt;segment&gt;</li>
</ul>

<hr>

<h2>📌 Notes</h2>

<ul>
<li>FFmpeg must be installed</li>
<li>Docker must be running</li>
<li>.env file must be configured correctly</li>
<li>Worker must run for video processing</li>
</ul>

<hr>


</body>
</html>

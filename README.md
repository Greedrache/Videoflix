<h1>🎬 Videoflix Backend</h1>

<p>Django REST API for a Netflix-style video streaming platform.</p>

<p>🌍 Live version:<br>
👉 <a href="https://tim-thiele.de" target="_blank">https://tim-thiele.de</a></p>

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

<h2>⚙️ Setup Instructions</h2>
<p>Before running the project, complete all the following steps in order:</p>

<h3>1. Clone Repository</h3>
<pre><code>git clone https://github.com/Greedrache/Vdeoflix .</code></pre>

<h3>2. Create Virtual Environment</h3>
<pre><code>python -m venv venv </code></pre>
<h4>Windows </h4>
<pre><code>.\venv\Scripts\activate </code></pre>
<h4> Mac / Linux </h4>
<pre><code>source venv/bin/activate </code></pre>


<h3>3. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>4. Start Docker (Database + Redis)</h3>
<pre><code>docker-compose up -d</code></pre>

<h3>5. Configure Environment Variables (.env)</h3>

<h4>Windows</h4>
<pre><code>SET SECRET_KEY=your_secure_key
SET DJANGO_DEBUG=True

SET POSTGRES_DB=postgres
SET POSTGRES_USER=postgres
SET POSTGRES_PASSWORD=postgres
SET POSTGRES_HOST=localhost
SET POSTGRES_PORT=5432

SET REDIS_URL=redis://localhost:6379/1

SET EMAIL_HOST=smtp.gmail.com
SET EMAIL_PORT=587
SET EMAIL_USE_TLS=True
SET EMAIL_HOST_USER=your.email@gmail.com
SET EMAIL_HOST_PASSWORD=your_app_password
</code></pre>

<h4>Mac / Linux</h4>
<pre><code>export SECRET_KEY=your_secure_key
export DJANGO_DEBUG=True

export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

export REDIS_URL=redis://localhost:6379/1

export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=your.email@gmail.com
export EMAIL_HOST_PASSWORD=your_app_password
</code></pre>

<h3>6. Set Up Database</h3>
<pre><code>python manage.py makemigrations
python manage.py migrate
</code></pre>

<h3>Optional: Create Admin User</h3>
<pre><code>python manage.py createsuperuser</code></pre>

<hr>

<h2>▶️ Running the Project</h2>
<p>Only after completing the steps above:</p>

<h3>Terminal 1: Django Server</h3>
<pre><code>python manage.py runserver</code></pre>
<p>👉 Running on: http://127.0.0.1:8000</p>

<h3>Terminal 2: Background Worker (Video Conversion)</h3>
<pre><code>python manage.py rqworker default</code></pre>

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
<li>Docker must be running before starting the server</li>
<li>.env file must be configured correctly</li>
<li>Background worker must run for video processing</li>
</ul>

</body>
</html>

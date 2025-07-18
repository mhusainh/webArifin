# 🚀 Portfolio Website - Arifin

Sebuah website portfolio modern dan interaktif yang dibangun dengan Python Flask, menampilkan desain yang elegan dengan fitur dark mode, animasi smooth, dan UI yang responsif.

## ✨ Fitur Utama

- 🎨 **Desain Modern**: UI yang clean dan profesional dengan gradien yang menarik
- 🌙 **Dark/Light Mode**: Toggle tema dengan animasi smooth
- 📱 **Responsive Design**: Tampil sempurna di semua perangkat
- ⚡ **Animasi Interaktif**: Smooth scrolling, hover effects, dan loading animations
- 📊 **Progress Bars**: Visualisasi skill dengan animasi
- 📬 **Contact Form**: Form kontak yang functional dengan notifikasi
- 🗄️ **Database Integration**: Penyimpanan pesan ke MySQL database
- 🔐 **Admin Panel**: Dashboard admin untuk mengelola pesan
- 👤 **User Authentication**: Sistem login untuk admin
- 🎮 **Easter Egg**: Konami code untuk surprise effect
- 🔍 **SEO Friendly**: Struktur HTML yang optimal
- 🐳 **Docker Support**: Containerized deployment dengan Docker Compose
- 🚀 **Production Ready**: Nginx reverse proxy dengan security headers
- ⚙️ **Environment Configuration**: Flexible configuration dengan environment variables
- 📝 **Logging System**: Comprehensive application logging
- 💚 **Health Checks**: Container health monitoring

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.8+**
- **Flask 2.3.3** - Web framework
- **MySQL** - Database untuk menyimpan pesan dan user
- **mysql-connector-python** - MySQL driver
- **Jinja2** - Template engine

### Frontend
- **HTML5** - Struktur semantic
- **CSS3** - Styling dengan custom properties dan animations
- **JavaScript ES6+** - Interaktivitas dan DOM manipulation
- **Font Awesome** - Icons
- **Google Fonts** - Typography (Poppins)

### DevOps & Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy dan web server (production)
- **Environment Variables** - Configuration management

### Fitur Tambahan
- **Local Storage** - Menyimpan preferensi tema
- **Intersection Observer API** - Lazy loading animations
- **Service Worker Ready** - Siap untuk PWA
- **Health Checks** - Container monitoring
- **Logging System** - Application dan error logging

## 🚀 Cara Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/username/webArifin.git
cd webArifin
```

### 2. Setup Database

#### Option A: Docker (Recommended)

**Quick Start:**
```bash
docker compose up --build -d
```

**Requirements:**
- Docker Desktop atau Docker Engine
- Docker Compose

**Access:**
- Application: http://localhost:5000
- Admin Panel: http://localhost:5000/login (admin/admin123)

📖 **Lihat file `DOCKER_SETUP.md` untuk panduan lengkap Docker**

#### Option B: Manual Setup dengan MySQL

**Penting**: Aplikasi sekarang menggunakan MySQL sebagai database.

1. **Buat Virtual Environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install MySQL Server:**
   - Download dan install MySQL Server dari [mysql.com](https://dev.mysql.com/downloads/mysql/)
   - Atau gunakan XAMPP/WAMP yang sudah include MySQL

4. **Create Database (Optional):**
   ```sql
   CREATE DATABASE portfolio_db;
   ```

5. **Configure Database:**
   - Edit `config.py` dan sesuaikan dengan setup MySQL Anda
   - Masukkan password MySQL yang benar

6. **Detailed Setup:**
   - Lihat `MYSQL_SETUP.md` untuk panduan lengkap setup MySQL

### 3. Jalankan Aplikasi

#### Dengan Docker:
```bash
docker compose up --build -d
```

#### Manual Setup:
```bash
python app.py
```

### 4. Buka Browser
Kunjungi `http://localhost:5000`

### 5. Login Admin
- URL: `http://localhost:5000/login`
- Username: `admin`
- Password: `admin123`

## 📁 Struktur Proyek

```
webArifin/
│
├── app.py                    # Aplikasi Flask utama
├── config.py                 # Konfigurasi database & Flask
├── requirements.txt          # Dependencies Python
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Production Docker setup
├── docker-compose.dev.yml   # Development Docker setup
├── .dockerignore            # Docker ignore file
├── .env.example             # Environment variables template
├── nginx.conf               # Nginx configuration
├── DOCKER_SETUP.md          # Panduan setup Docker
├── MYSQL_SETUP.md           # Panduan setup MySQL manual
├── README.md                # Dokumentasi proyek
│
├── mysql-init/              # Database initialization
│   └── 01-init.sql
│
├── templates/               # Template HTML
│   ├── index.html          # Main HTML template
│   ├── login.html          # Admin login page
│   └── admin.html          # Admin dashboard
│
├── static/                  # File CSS, JS, gambar
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── script.js       # JavaScript functionality
│
└── logs/                    # Application logs (auto-created)
```

## 🎨 Kustomisasi

### Mengubah Data Portfolio
Edit data di `app.py` pada variabel `portfolio_data`:

```python
portfolio_data = {
    "name": "Nama Anda",
    "title": "Jabatan Anda",
    "bio": "Deskripsi singkat tentang Anda",
    # ... data lainnya
}
```

### Mengubah Warna Tema
Edit CSS custom properties di `static/css/style.css`:

```css
:root {
    --primary-color: #667eea;    /* Warna utama */
    --secondary-color: #764ba2;  /* Warna sekunder */
    --accent-color: #f093fb;     /* Warna aksen */
    /* ... variabel lainnya */
}
```

### Menambah Skill Baru
Tambahkan skill di array `skills` dalam `portfolio_data`:

```python
{
    "name": "Nama Skill",
    "level": 85,  # Persentase (0-100)
    "icon": "🔥"  # Emoji icon
}
```

## 🌟 Fitur Khusus

### Dark Mode
- Toggle otomatis menyimpan preferensi di localStorage
- Animasi smooth saat pergantian tema
- Ikon berubah sesuai tema aktif

### Animasi
- Intersection Observer untuk lazy loading
- Progress bar animasi saat scroll
- Floating icons dengan parallax effect
- Smooth scrolling navigation

### Easter Egg
Coba masukkan Konami Code: `↑↑↓↓←→←→BA` untuk efek surprise! 🎉

## 📱 Browser Support

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Proyek ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.

## 👨‍💻 Author

**Arifin**
- Email: arifin@example.com
- GitHub: [@arifin](https://github.com/arifin)
- LinkedIn: [Arifin](https://linkedin.com/in/arifin)

## 🙏 Acknowledgments

- Font Awesome untuk icons
- Google Fonts untuk typography
- Flask community untuk framework yang amazing
- Semua developer yang berkontribusi pada open source

---

⭐ Jika proyek ini membantu Anda, jangan lupa berikan star!
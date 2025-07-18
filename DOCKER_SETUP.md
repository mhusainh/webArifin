# Docker Setup Guide

Panduan lengkap untuk menjalankan aplikasi Portfolio menggunakan Docker dan Docker Compose.

## Prasyarat

- Docker Desktop (Windows/Mac) atau Docker Engine (Linux)
- Docker Compose (biasanya sudah termasuk dalam Docker Desktop)
- Git (untuk clone repository)

### Instalasi Docker

**Windows/Mac:**
1. Download dan install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Jalankan Docker Desktop
3. Pastikan Docker berjalan dengan menjalankan: `docker --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd webArifin
```

### 2. Jalankan dengan Docker Compose

**Production Mode:**
```bash
docker compose up --build -d
```

**Development Mode:**
```bash
docker compose -f docker-compose.dev.yml up --build -d
```

### 3. Akses Aplikasi

- **Aplikasi Flask:** http://localhost:5000
- **Dengan Nginx (Production):** http://localhost
- **Admin Panel:** http://localhost:5000/login
  - Username: `admin`
  - Password: `admin123`

## Konfigurasi

### Environment Variables

Buat file `.env` dari template:
```bash
cp .env.example .env
```

Edit file `.env` sesuai kebutuhan:
```env
# Database Configuration
DB_HOST=mysql
DB_USER=portfolio_user
DB_PASSWORD=portfolio_password
DB_NAME=portfolio_db

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Docker Compose Files

1. **docker-compose.yml** - Production setup dengan Nginx
2. **docker-compose.dev.yml** - Development setup tanpa Nginx

## Perintah Docker Compose

### Menjalankan Services
```bash
# Production
docker compose up -d

# Development
docker compose -f docker-compose.dev.yml up -d

# Dengan rebuild
docker compose up --build -d
```

### Melihat Logs
```bash
# Semua services
docker compose logs -f

# Service tertentu
docker compose logs -f web
docker compose logs -f mysql
```

### Menghentikan Services
```bash
# Stop services
docker compose down

# Stop dan hapus volumes
docker compose down -v
```

### Mengakses Container
```bash
# Masuk ke container web
docker compose exec web bash

# Masuk ke MySQL
docker compose exec mysql mysql -u portfolio_user -p portfolio_db
```

## Struktur Docker

### Services

1. **mysql** - MySQL 8.0 database
   - Port: 3306
   - Volume: mysql_data
   - Health check enabled

2. **web** - Flask application
   - Port: 5000
   - Depends on MySQL
   - Auto-restart enabled

3. **nginx** - Reverse proxy (production only)
   - Port: 80, 443
   - Load balancing
   - Security headers
   - Rate limiting

### Volumes

- `mysql_data` - Persistent MySQL data
- `./logs` - Application logs
- `./mysql-init` - Database initialization scripts

### Networks

- `portfolio_network` - Internal network untuk komunikasi antar container

## Database Initialization

Database akan otomatis diinisialisasi dengan:
- Database: `portfolio_db`
- User: `portfolio_user`
- Tables: `messages`, `users`
- Default admin user

Script inisialisasi ada di `mysql-init/01-init.sql`

## Monitoring dan Debugging

### Health Checks
```bash
# Cek status containers
docker compose ps

# Cek health status
docker inspect portfolio_mysql --format='{{.State.Health.Status}}'
```

### Performance Monitoring
```bash
# Resource usage
docker stats

# Container processes
docker compose top
```

### Debugging
```bash
# Inspect container
docker compose exec web env

# Check database connection
docker compose exec web python -c "from app import get_db_connection; print(get_db_connection())"
```

## Production Deployment

### Security Considerations

1. **Environment Variables:**
   - Gunakan secrets management
   - Jangan commit file `.env`
   - Generate strong SECRET_KEY

2. **Database:**
   - Gunakan password yang kuat
   - Backup database secara berkala
   - Monitor koneksi database

3. **Nginx:**
   - Setup SSL/TLS certificates
   - Configure firewall
   - Enable access logs

### SSL/HTTPS Setup

1. Dapatkan SSL certificate (Let's Encrypt, dll)
2. Simpan di folder `ssl/`
3. Uncomment HTTPS server block di `nginx.conf`
4. Update domain name

### Backup Database
```bash
# Backup
docker compose exec mysql mysqldump -u portfolio_user -p portfolio_db > backup.sql

# Restore
docker compose exec -T mysql mysql -u portfolio_user -p portfolio_db < backup.sql
```

## Troubleshooting

### Common Issues

1. **Port sudah digunakan:**
   ```bash
   # Cek port yang digunakan
   netstat -tulpn | grep :5000
   
   # Ubah port di docker-compose.yml
   ports:
     - "5001:5000"  # Gunakan port 5001
   ```

2. **Database connection error:**
   ```bash
   # Cek MySQL container
   docker compose logs mysql
   
   # Test koneksi
   docker compose exec web ping mysql
   ```

3. **Permission issues:**
   ```bash
   # Fix ownership (Linux/Mac)
   sudo chown -R $USER:$USER logs/
   ```

4. **Container tidak start:**
   ```bash
   # Rebuild images
   docker compose build --no-cache
   
   # Remove old containers
   docker compose down
   docker system prune -f
   ```

### Logs Location

- Application logs: `logs/app.log`
- Docker logs: `docker compose logs`
- MySQL logs: `docker compose logs mysql`
- Nginx logs: `docker compose logs nginx`

## Development Workflow

1. **Code Changes:**
   - Edit files locally
   - Changes auto-reload (development mode)
   - Check logs: `docker compose logs -f web`

2. **Database Changes:**
   - Update `mysql-init/01-init.sql`
   - Recreate database: `docker compose down -v && docker compose up -d`

3. **Dependencies:**
   - Update `requirements.txt`
   - Rebuild: `docker compose build web`

## Performance Optimization

### Docker
- Use multi-stage builds
- Minimize image layers
- Use .dockerignore
- Enable BuildKit

### Application
- Enable gzip compression (Nginx)
- Use connection pooling
- Implement caching
- Monitor resource usage

### Database
- Optimize queries
- Add proper indexes
- Regular maintenance
- Monitor slow queries

---

**Catatan:** Untuk development, gunakan `docker-compose.dev.yml`. Untuk production, gunakan `docker-compose.yml` dengan Nginx.
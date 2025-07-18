# Setup MySQL untuk Portfolio Website

## Prasyarat
1. Install MySQL Server di komputer Anda
2. Install MySQL Workbench (opsional, untuk GUI)

## Langkah-langkah Setup

### 1. Install MySQL Server
- Download MySQL dari https://dev.mysql.com/downloads/mysql/
- Install dengan mengikuti wizard
- Catat username dan password yang Anda buat

### 2. Konfigurasi Database

#### Opsi A: Menggunakan Command Line
```bash
# Login ke MySQL
mysql -u root -p

# Buat database (opsional, aplikasi akan membuatnya otomatis)
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Buat user khusus (opsional)
CREATE USER 'portfolio_user'@'localhost' IDENTIFIED BY 'password_anda';
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Opsi B: Menggunakan MySQL Workbench
1. Buka MySQL Workbench
2. Connect ke MySQL Server
3. Buat database baru dengan nama `portfolio_db`
4. Set charset ke `utf8mb4` dan collation ke `utf8mb4_unicode_ci`

### 3. Konfigurasi Aplikasi

1. Buka file `config.py`
2. Update konfigurasi database:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # atau user yang Anda buat
    'password': 'password_anda',  # masukkan password MySQL
    'database': 'portfolio_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
```bash
python app.py
```

## Troubleshooting

### Error: "Access denied for user"
- Pastikan username dan password benar
- Pastikan user memiliki privileges untuk database

### Error: "Can't connect to MySQL server"
- Pastikan MySQL service berjalan
- Periksa host dan port (default: localhost:3306)

### Error: "Unknown database"
- Database akan dibuat otomatis saat pertama kali menjalankan aplikasi
- Atau buat manual menggunakan command di atas

## Keamanan untuk Production

1. Gunakan environment variables untuk kredensial:
```bash
export DB_HOST=localhost
export DB_USER=portfolio_user
export DB_PASSWORD=secure_password
export DB_NAME=portfolio_db
```

2. Buat user database khusus dengan privileges terbatas
3. Gunakan SSL connection untuk koneksi database
4. Backup database secara berkala

## Migrasi dari SQLite

Jika Anda sebelumnya menggunakan SQLite:
1. Data lama di `portfolio.db` tidak akan terbaca
2. Aplikasi akan membuat tabel baru di MySQL
3. User admin default akan dibuat otomatis (username: arifin123, password: arifin 123)
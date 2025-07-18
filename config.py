import os

# Database Configuration
# Prioritas: Environment Variables > Default Values

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # Masukkan password MySQL Anda di sini untuk development
    'database': os.getenv('DB_NAME', 'portfolio_db'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
}

# Flask Configuration
FLASK_CONFIG = {
    'SECRET_KEY': os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production'),
    'DEBUG': os.getenv('FLASK_ENV', 'development') == 'development',
    'HOST': os.getenv('FLASK_HOST', '0.0.0.0'),
    'PORT': int(os.getenv('FLASK_PORT', '5000'))
}

# Logging Configuration
LOGGING_CONFIG = {
    'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
    'LOG_FILE': os.getenv('LOG_FILE', 'logs/app.log')
}
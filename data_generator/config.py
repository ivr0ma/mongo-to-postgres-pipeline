import os

# Настройки подключения к базе данных
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "project_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "your_password"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

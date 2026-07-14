import psycopg

from app.config.settings import settings


connection = psycopg.connect(
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    dbname=settings.POSTGRES_DB,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
)

print("Connected to PostgreSQL")

connection.close()
import requests
import os
import logging
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

API_URL = "https://api.open-meteo.com/v1/forecast"

CITY = "Tashkent"
TIMEZONE = "Asia/Tashkent"

def fetch_weather() -> dict:
    params = {
        "latitude": 41.2995,
        "longitude": 69.2401,
        "hourly": "temperature_2m",
        "timezone": TIMEZONE,
        "forecast_days": 3,
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("Не удалось получить данные: %s", exc)
        raise
        
    data = response.json()
    logger.info("Получено %d записей", len(data["hourly"]["time"]))
    return data

def transform(data: dict) -> list:
    hourly = data["hourly"]
    rows = []

    for time, temperature in zip(
        hourly["time"],
        hourly["temperature_2m"],
    ):
        naive_time = datetime.fromisoformat(time)
        forecast_time = naive_time.replace(
            tzinfo=ZoneInfo(TIMEZONE)
        )
        rows.append(
            (
                CITY,
                forecast_time,
                temperature,
            )
        )
    return rows

def load(rows:list[tuple]) -> int: 
    try:
        connection = psycopg2.connect(
            host = os.getenv("POSTGRES_HOST", "localhost"),
            port = os.getenv("POSTGRES_PORT", "5432"),
            dbname = os.getenv("POSTGRES_DB"),
            user = os.getenv("POSTGRES_USER"),
            password = os.getenv("POSTGRES_PASSWORD"),
        )



        sql = """
            INSERT INTO weather_hourly (
                city,
                forecast_time,
                temperature
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (city, forecast_time)
            DO UPDATE SET
                temperature = EXCLUDED.temperature;
        """
        with connection:
            with connection.cursor() as cursor:
                cursor.executemany(sql, rows)

    finally:
        connection.close()
    return len(rows)

def main() -> None:
    data = fetch_weather()
    rows = transform(data)
    logger.info("Сохранено %d строк", load(rows))

if __name__ == '__main__':
    main()
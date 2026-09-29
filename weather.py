import requests
import json
import pathlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def fetch_weather() -> dict:
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 41.2995,
        "longitude": 69.2401,
        "hourly": "temperature_2m",
        "timezone": "Asia/Tashkent",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("Не удалось получить данные: %s", exc)
        raise
        
    data = response.json()
    logger.info("Получено %d записей", len(data["hourly"]["time"]))
    return data

def save_raw(data: dict, path: str) -> None:
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    logger.info("Сохранено в %s", path)

if __name__ == '__main__':
    save_raw(fetch_weather(), "data/raw_weather.json")
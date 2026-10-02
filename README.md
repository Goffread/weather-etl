# Weather Data Pipeline

Небольшой учебный Data Engineering-проект, который получает почасовой прогноз погоды из Open-Meteo и сохраняет данные в PostgreSQL.

## Как работает проект

Open-Meteo API
      ↓
    Python
      ↓
  PostgreSQL
      ↓
 SQL-анализ

Python получает данные из API, преобразует их в нужный формат и загружает в PostgreSQL. Повторный запуск не создаёт дубликаты данных.

## Возможности

* получение погодных данных из Open-Meteo API;
* загрузка данных в PostgreSQL;
* запуск PostgreSQL в Docker;
* защита от повторной загрузки одинаковых данных;
* SQL-анализ загруженных данных;
* проверка дубликатов и пропущенных часов.

## Стек

* Python
* PostgreSQL
* Docker / Docker Compose
* SQL
* psycopg2
* Open-Meteo API
* Git / GitHub

## Структура проекта

.
├── weather.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_analysis.sql
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md

## Запуск проекта

### 1. Клонировать репозиторий

git clone https://github.com/Goffread/weather-etl.git
cd weather-etl

### 2. Создать `.env`

Создайте файл `.env` на основе `.env.example` и укажите необходимые переменные окружения.

Например:

POSTGRES_PASSWORD=your_password

### 3. Запустить PostgreSQL

docker compose up -d

Проверить состояние контейнера:

docker compose ps

### 4. Создать таблицу

sql/01_create_tables.sql

### 5. Установить зависимости Python

pip install -r requirements.txt

### 6. Запустить загрузку данных

python weather.py

После выполнения данные из Open-Meteo должны появиться в таблице `weather_hourly`.

### 7. Выполнить SQL-анализ

Запросы находятся в:

sql/02_analysis.sql

Они позволяют проверить загруженные данные, в том числе наличие дубликатов и пропущенных часов.

## Воспроизводимость

Проект проверен запуском в отдельной директории из чистого клона репозитория.

Для повторного запуска необходимо:

1. клонировать репозиторий;
2. создать `.env`;
3. запустить PostgreSQL через Docker Compose;
4. создать таблицу из `sql/01_create_tables.sql`;
5. установить Python-зависимости;
6. запустить `weather.py`;
7. выполнить SQL-запросы из `sql/02_analysis.sql`.

## Результат

Проект демонстрирует базовый ETL-пайплайн:

**API → Python → PostgreSQL → SQL-анализ**

и основные навыки, необходимые для начального Data Engineering-проекта.

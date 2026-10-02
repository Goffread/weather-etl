# Weather Data Pipeline

Небольшой учебный Data Engineering-проект, который получает почасовой прогноз погоды из Open-Meteo и сохраняет данные в PostgreSQL.

## Как работает проект

```text
Open-Meteo API
      ↓
    Python
      ↓
  PostgreSQL
      ↓
 SQL-анализ
```

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

```text
.
├── weather.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_analysis.sql
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Goffread/weather-etl.git
cd weather-etl
```

### 2. Создать `.env`

Создайте файл `.env` на основе `.env.example` и укажите необходимые переменные окружения.

Например:

```env
POSTGRES_USER=your_nickname
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Не добавляйте настоящий `.env` в Git. Он должен находиться в `.gitignore`.

### 3. Запустить PostgreSQL

```bash
docker compose up -d
```

Проверить состояние контейнера:

```bash
docker compose ps
```

### 4. Создать таблицу

Подключитесь к PostgreSQL и выполните SQL из:

```text
sql/01_create_tables.sql
```

### 5. Установить зависимости Python

```bash
pip install -r requirements.txt
```

### 6. Запустить загрузку данных

```bash
python weather.py
```

После выполнения данные из Open-Meteo должны появиться в таблице `weather_hourly`.

### 7. Выполнить SQL-анализ

Запросы находятся в:

```text
sql/02_analysis.sql
```

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

Пример вывода из таблицы weather_hourly:

```bash
SELECT city,
       forecast_time,
       temperature 
  FROM weather_hourly;

 city   |     forecast_time      | temperature 
----------+------------------------+-------------
 Tashkent | 2026-09-29 19:00:00+00 |       17.30
 Tashkent | 2026-09-29 20:00:00+00 |       16.70
 Tashkent | 2026-09-29 21:00:00+00 |       16.40
 Tashkent | 2026-09-29 22:00:00+00 |       15.70
 Tashkent | 2026-09-29 23:00:00+00 |       15.00
 Tashkent | 2026-09-30 00:00:00+00 |       14.60
 Tashkent | 2026-09-30 01:00:00+00 |       14.20
 Tashkent | 2026-09-30 02:00:00+00 |       14.70
 Tashkent | 2026-10-01 19:00:00+00 |       14.30
 Tashkent | 2026-10-01 20:00:00+00 |       14.40
 Tashkent | 2026-10-01 21:00:00+00 |       14.10
 Tashkent | 2026-10-01 22:00:00+00 |       14.00
 ```

 Ограничения:
 Один город, только температура, нет оркестрации.
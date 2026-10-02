-- 1. Ежедневная статистика
SELECT 
    (forecast_time AT TIME ZONE 'Asia/Tashkent')::date AS forecast_date,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature
FROM weather_hourly
GROUP BY forecast_date
ORDER BY forecast_date;

-- 2. Температура выше средней температу
SELECT (forecast_time AT TIME ZONE 'Asia/Tashkent') AS forecast_time,
        temperature
  FROM weather_hourly
 WHERE temperature > (SELECT AVG(temperature) 
                       FROM weather_hourly);
 ORDER BY 1;

-- 3. Проверка дублей по city + forecast_time
SELECT city, forecast_time, COUNT(*) AS count
FROM weather_hourly
GROUP BY city, forecast_time
HAVING COUNT(*) > 1;

-- 4. Поиск пропущенных часов
WITH hours AS (
    SELECT generate_series(
        MIN(forecast_time),
        MAX(forecast_time),
        INTERVAL '1 hour'
    ) AS hour
    FROM weather_hourly
)
SELECT hours.hour
FROM hours
LEFT JOIN weather_hourly AS wh
    ON hours.hour = wh.forecast_time
WHERE wh.forecast_time IS NULL
ORDER BY hours.hour;
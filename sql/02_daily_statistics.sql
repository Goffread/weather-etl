SELECT 
    (forecast_time AT TIME ZONE 'Asia/Tashkent')::date AS forecast_date,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature
FROM weather_hourly
GROUP BY forecast_date
ORDER BY forecast_date;
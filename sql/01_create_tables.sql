CREATE TABLE weather_hourly (
    city          VARCHAR(100) NOT NULL,
    forecast_time TIMESTAMPTZ NOT NULL,
    temperature   NUMERIC(5,2),
    PRIMARY KEY (city, forecast_time)
);
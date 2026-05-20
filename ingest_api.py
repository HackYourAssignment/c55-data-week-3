"""API ingestion helpers for fetching weather data from Open-Meteo."""
# Step 2 — Tasks 1 & 2: Error Handling + API Ingestion
# fetch_with_retry handles transient network errors (Task 1).
# fetch_api_records calls it and shapes the response into flat dicts (Task 2).
import logging
import time

import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


def fetch_with_retry(url: str, params: dict, max_retries: int = 3, timeout: int = 10) -> dict:
    """Fetch url with exponential backoff on transient errors.

    Retry on: ConnectionError, Timeout, 5xx status codes.
    Fail immediately on: 4xx status codes.
    Log each retry attempt with the error and delay.
    """

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code in RETRYABLE_STATUS_CODES:
                if attempt == max_retries - 1:
                    response.raise_for_status()

                wait_time = 2 ** attempt
                logger.warning(
                    "Server error %s. Retrying in %s seconds.",
                    response.status_code,
                    wait_time,
                )
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt
            logger.warning(
                "Network error: %s. Retrying in %s seconds.",
                error,
                wait_time,
            )
            time.sleep(wait_time)

    raise RuntimeError("Could not fetch data after all retries.")


def fetch_api_records() -> list[dict]:
    """Fetch hourly weather from Open-Meteo and return flat dicts.

    Returns a list of dicts with keys: station, timestamp, temperature_c, humidity_pct.
    Returns [] if the API returns no data (do not raise an exception).
    """
    params = {
        "latitude": 55.67,
        "longitude": 12.56,
        "hourly": "temperature_2m,relative_humidity_2m",
        "forecast_days": 7,
    }

    try:
        data = fetch_with_retry(API_URL, params)
    except RuntimeError:
        logger.error("Failed to fetch data from API after retries.")
        return []

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])

    if not times or not temperatures or not humidities:
        return []
    records = []

    for time_str, temp, humidity in zip(times, temperatures, humidities):
        record = {
            "station": "Open-Meteo Copenhagen",
            "timestamp": time_str,
            "temperature_c": temp,
            "humidity_pct": humidity,
        }
        records.append(record)
    return records

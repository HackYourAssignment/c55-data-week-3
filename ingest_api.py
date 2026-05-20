# Step 2 — Tasks 1 & 2: Error Handling + API Ingestion
# fetch_with_retry handles transient network errors (Task 1).
# fetch_api_records calls it and shapes the response into flat dicts (Task 2).

import logging
import time
import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_with_retry(url: str, params: dict, max_retries: int = 3, timeout: int = 10) -> dict:
    """Fetch URL with exponential backoff on transient errors."""

    delay = 1

    for attempt in range(max_retries):
        try:
            logger.info(f"Request attempt {attempt + 1} to {url}")

            response = requests.get(url, params=params, timeout=timeout)

            # Fail immediately on client errors (4xx)
            if 400 <= response.status_code < 500:
                logger.error(f"Client error {response.status_code}")
                response.raise_for_status()

            # Retry on server errors (5xx)
            if 500 <= response.status_code < 600:
                logger.warning(f"Server error {response.status_code}, retrying...")
                raise requests.HTTPError(f"Server error: {response.status_code}")

            return response.json()

        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:

            logger.warning(f"Attempt {attempt + 1} failed: {e}")

            if attempt == max_retries - 1:
                logger.error("Max retries reached. Returning empty response.")
                return {}

            time.sleep(delay)
            delay *= 2  # exponential backoff


def fetch_api_records() -> list[dict]:
    """Fetch hourly weather from Open-Meteo and return flat dicts."""

    params = {
        "latitude": 55.67,
        "longitude": 12.56,
        "hourly": "temperature_2m,relative_humidity_2m",
        "forecast_days": 7,
    }

    data = fetch_with_retry(API_URL, params)

    if not data or "hourly" not in data:
        logger.warning("No data returned from API")
        return []

    hourly = data["hourly"]

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    humidity = hourly.get("relative_humidity_2m", [])

    records = []

    for i in range(len(times)):
        records.append({
            "station": "Open-Meteo Copenhagen",
            "timestamp": times[i],
            "temperature_c": temps[i],
            "humidity_pct": humidity[i],
        })

    logger.info(f"Fetched {len(records)} API records")
    return records
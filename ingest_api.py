# Step 2 — Tasks 1 & 2: Error Handling + API Ingestion
# fetch_with_retry handles transient network errors (Task 1).
# fetch_api_records calls it and shapes the response into flat dicts (Task 2).
import logging
import time

import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_with_retry(url: str, params: dict, max_retries: int = 3, timeout: int = 10) -> dict:
    """Fetch url with exponential backoff on transient errors.

    Retry on: ConnectionError, Timeout, 5xx status codes.
    Fail immediately on: 4xx status codes.
    Log each retry attempt with the error and delay.
    """
    # TODO: implement retry loop with exponential backoff
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code >= 500:
                raise requests.HTTPError(f"Server error: {response.status_code}")
            elif response.status_code >= 400:
                response.raise_for_status()  # Will raise HTTPError for 4xx
            return response.json()
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            if attempt == max_retries or isinstance(e, requests.HTTPError) and e.response.status_code < 500:
                logger.error(f"Request failed after {attempt} attempts: {e}")
                raise
            delay = 2 ** (attempt - 1)  # Exponential backoff: 1s, 2s, 4s...
            logger.warning(f"Request error: {e}. Retrying in {delay} seconds... (Attempt {attempt}/{max_retries})")
            time.sleep(delay)
    raise RuntimeError("Exceeded maximum retry attempts")


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
    # TODO:
    # - Call fetch_with_retry with API_URL and params
    # - The API returns {"hourly": {"time": [...], "temperature_2m": [...], "relative_humidity_2m": [...]}}
    # - Flatten to a list of dicts; set station="Open-Meteo Copenhagen" for all records
    for attempt in range(1, 4):
        try:
            data = fetch_with_retry(API_URL, params)
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            hums = hourly.get("relative_humidity_2m", [])
            records = []
            for time_str, temp, hum in zip(times, temps, hums):
                records.append({
                    "station": "Open-Meteo Copenhagen",
                    "timestamp": time_str,
                    "temperature_c": temp,
                    "humidity_pct": hum,
                })
            return records
        except Exception as e:
            logger.error(f"Failed to fetch API records: {e}")
            return []
    raise RuntimeError("Exceeded maximum retry attempts")

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

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if 400 <= response.status_code < 500:
                response.raise_for_status()

            if response.status_code >= 500:
                raise requests.HTTPError(f"Server error: {response.status_code}", response=response)

            return response.json()
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            is_last_attempt = attempt == max_retries
            if isinstance(e, requests.HTTPError):
                response = e.response
                if response is not None and 400 <= response.status_code < 500:
                    raise  # Do not retry on client errors
            if is_last_attempt:
                raise
            delay = 2 ** attempt
            logger.warning("Retry %s%s after error: %s. waiting %s seconds.", attempt + 1, max_retries, e, delay)
            time.sleep(delay)


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
    data = fetch_with_retry(API_URL, params)
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])

    if not times:
        return []
    records = []
    for timestamp, temp, humidity in zip(times, temperatures, humidities):
        records.append({
            "station": "Open-Meteo Copenhagen",
            "timestamp": timestamp,
            "temperature_c": temp,
            "humidity_pct": humidity
        })
    return records

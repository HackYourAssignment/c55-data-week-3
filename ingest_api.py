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
    attempt =0

    while attempt <= max_retries:
        try:
            logger.info(f"Attempt {attempt + 1} to fetch data")

            response = requests.get(url, params=params, timeout=timeout)

            if 400 <= response.status_code < 500:
                logger.error(f"Client error {response.status_code}: {response.text}")
                return None

            if response.status_code >= 500:
                raise requests.exceptions.HTTPError(f"Server error {response.status_code}")

            return response.json()

        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError) as e:
            
            logger.warning(f"Error on attempt {attempt + 1}: {e}")

            attempt += 1

            if attempt > max_retries:
                logger.error("Max retries reached. Giving up.")
                return None

            sleep_time = 2 ** attempt
            logger.info(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)


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

    if not data or "hourly" not in data:
        logger.warning("No data returned from API")
        return []

    hourly = data["hourly"]

    times = hourly.get("time", [])
    print(len(times))
    temps = hourly.get("temperature_2m", [])
    humidity = hourly.get("relative_humidity_2m", [])

    records = []

    for i in range(len(times)):
        record = {
            "station": "Open-Meteo Copenhagen",
            "timestamp": times[i],
            "temperature_c": temps[i] if i < len(temps) else None,
            "humidity_pct": humidity[i] if i < len(humidity) else None,
        }
        records.append(record)

    return records
    
if __name__ == "__main__":
     #print("RUNNING FILE...")
     logging.basicConfig(level=logging.INFO)

     records = fetch_api_records()
     print(f"Fetched {len(records)} records")
     
     print(records[:2])  

     

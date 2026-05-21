import logging
import time
import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_with_retry(
    url: str, params: dict, max_retries: int = 3, timeout: int = 10
) -> dict:
    """Fetch url with exponential backoff on transient errors.

    Retry on: ConnectionError, Timeout, 5xx status codes.
    Fail immediately on: 4xx status codes.
    Log each retry attempt with the error and delay.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code < 500:
                logger.error(
                    f"Client error {response.status_code}. Failing immediately."
                )
                raise

            error_msg = f"Server error {response.status_code}"
            error_type = error_msg

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            error_type = type(e).__name__

        if attempt == max_retries - 1:
            logger.error(
                f"Max retries reached. Final attempt failed with {error_type}."
            )
            raise

        wait_time = 2**attempt
        logger.warning(
            f"Attempt {attempt + 1} failed ({error_type}). Retrying in {wait_time}s..."
        )
        time.sleep(wait_time)

    raise RuntimeError("unreachable")


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
        data = fetch_with_retry(API_URL, params=params)
    except Exception as e:
        logger.error(f"Failed to fetch data from API: {e}")
        return []

    # Task 2: Robust parsing and flattening
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])

    if not times or not temps or not humidities:
        logger.warning(
            "API response structure was missing expected hourly data data arrays."
        )
        return []

    return [
        {
            "station": "Open-Meteo Copenhagen",
            "timestamp": ts,
            "temperature_c": temp,
            "humidity_pct": hum,
        }
        for ts, temp, hum in zip(times, temps, humidities, strict=True)
    ]

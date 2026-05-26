"""API ingestion helpers for fetching weather data from Open-Meteo."""

import logging
import time

import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


def fetch_with_retry(
    url: str,
    params: dict,
    max_retries: int = 3,
    timeout: int = 10,
) -> dict:
    """Fetch URL with exponential backoff on transient errors.

    Retry on ConnectionError, Timeout, and selected 5xx status codes.
    Fail immediately on non-retryable HTTP errors.
    """

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code in RETRYABLE_STATUS_CODES:
                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Could not fetch data after {max_retries} retries. "
                        f"Last status code: {response.status_code}"
                    )

                wait_time = 2**attempt
                logger.warning(
                    "Server error %s. Retrying in %s seconds.",
                    response.status_code,
                    wait_time,
                )
                time.sleep(wait_time)
                continue

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                raise RuntimeError(
                    f"Non-retryable HTTP error: {response.status_code}"
                ) from error

            return response.json()

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as error:
            if attempt == max_retries - 1:
                raise RuntimeError(
                    f"Could not fetch data after {max_retries} retries."
                ) from error

            wait_time = 2**attempt
            logger.warning(
                "Network error: %s. Retrying in %s seconds.",
                error,
                wait_time,
            )
            time.sleep(wait_time)

    raise RuntimeError("Could not fetch data after all retries.")


def fetch_api_records() -> list[dict]:
    """Fetch hourly weather from Open-Meteo and return flat dictionaries.

    Returns a list of dictionaries with keys:
    station, timestamp, temperature_c, humidity_pct.

    Returns an empty list if the API returns no usable data or if fetching fails.
    """

    params = {
        "latitude": 55.67,
        "longitude": 12.56,
        "hourly": "temperature_2m,relative_humidity_2m",
        "forecast_days": 7,
    }

    try:
        data = fetch_with_retry(API_URL, params)
    except RuntimeError as error:
        logger.error("Failed to fetch data from API after retries: %s", error)
        return []

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])

    if not times or not temperatures or not humidities:
        return []

    records = []

    for time_str, temperature, humidity in zip(times, temperatures, humidities):
        records.append(
            {
                "station": "Open-Meteo Copenhagen",
                "timestamp": time_str,
                "temperature_c": temperature,
                "humidity_pct": humidity,
            }
        )

    return records

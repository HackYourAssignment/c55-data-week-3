# Step 3 — Task 3: File Reading
# Read the messy CSV and normalize each row into the same dict format
# that fetch_api_records() produces, so validate_records() can handle both sources.
import csv
from pathlib import Path


def convert_float(value: str) -> float:
    """Convert value to float, or return original if conversion fails."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return value
    

def convert_int(value: str) -> int:
    """Convert value to int, or return original if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return value

def read_csv_records(path: Path) -> list[dict]:
    """Read weather_stations.csv and return normalized records.

    Returns a list of dicts with keys: station, timestamp, temperature_c, humidity_pct.

    Rules:
    - Open with newline="" and encoding="utf-8".
    - Use csv.DictReader.
    - Convert temperature_c to float and humidity_pct to int where possible.
    - Leave unconvertible values (e.g. "N/A", "") as-is so validation can catch them.
    """
    records = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "station": row.get("station", ""),
                "timestamp": row.get("timestamp", ""),
                "temperature_c": convert_float(row.get("temperature_c", "")),
                "humidity_pct": convert_int(row.get("humidity_pct", "")),
                })
             
    return records

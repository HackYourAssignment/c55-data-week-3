# Step 3 — Task 3: File Reading
# Read the messy CSV and normalize each row into the same dict format
# that fetch_api_records() produces, so validate_records() can handle both sources.
import csv
from pathlib import Path


def try_parse_float(value: str):
    try:
        return float(value)
    except ValueError:
        return value


def try_parse_int(value: str):
    try:
        return int(value)
    except ValueError:
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
    # TODO: implement CSV reading and normalization
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            record = {
                "station": row.get("station", "").strip(),
                "timestamp": row.get("timestamp", "").strip(),
                "temperature_c": try_parse_float(row.get("temperature_c", "").strip()),
                "humidity_pct": try_parse_int(row.get("humidity_pct", "").strip()),
            }
            records.append(record)
        return records
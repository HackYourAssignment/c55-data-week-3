# Step 3 — Task 3: File Reading
# Read the messy CSV and normalize each row into the same dict format
# that fetch_api_records() produces, so validate_records() can handle both sources.
import csv
from pathlib import Path


def read_csv_records(path: Path) -> list[dict]:
    """Read weather_stations.csv and return normalized records."""

    records = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            record = {
                "station": row.get("station"),
                "timestamp": row.get("timestamp"),
                "temperature_c": row.get("temperature_c"),
                "humidity_pct": row.get("humidity_pct"),
            }

            try:
                record["temperature_c"] = float(record["temperature_c"])
            except (TypeError, ValueError):
                pass

            try:
                record["humidity_pct"] = int(record["humidity_pct"])
            except (TypeError, ValueError):
                pass

            records.append(record)

    return records
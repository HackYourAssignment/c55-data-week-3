# Step 3 — Task 3: File Reading
# Read the messy CSV and normalize each row into the same dict format
# that fetch_api_records() produces, so validate_records() can handle both sources.
import csv
from pathlib import Path

def convert_float(value):
    if value is None:
        return value
    value = value.strip()
    if value == "" or value.upper() == "N/A":
        return value
    try:
        return float(value)
    except ValueError:
        return value


def convert_int(value):
    if value is None:
        return value
    value = value.strip()
    if value == "" or value.upper() == "N/A":
        return value
    try:
        return int(float(value))
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
def read_csv_records(path: Path) -> list[dict]:
    records = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            record = {
                "station": row.get("station"),
                "timestamp": row.get("timestamp"),
                "temperature_c": convert_float(row.get("temperature_c")),
                "humidity_pct": convert_int(row.get("humidity_pct")),
            }
            records.append(record)

    return records

with open("data/weather_stations.csv", newline="") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i <3:
         pass

if __name__ == "__main__":

    data = read_csv_records(Path("data/weather_stations.csv"))
    print(len(data))
    print(data[:3])
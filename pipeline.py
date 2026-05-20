import json
import logging
from pathlib import Path

from database import (
    count_readings,
    create_tables,
    get_connection,
    insert_raw,
    upsert_readings,
)
from ingest_api import fetch_api_records
from ingest_files import read_csv_records
from validate import validate_records


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")
CSV_PATH = Path("data/weather_stations.csv")


def run_pipeline() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. Fetch data
    api_records = fetch_api_records()
    csv_records = read_csv_records(CSV_PATH)

    # 2. Validate FIRST (important fix)
    valid_api, invalid_api = validate_records(api_records, "api")
    valid_csv, invalid_csv = validate_records(csv_records, "csv")

    valid_records = valid_api + valid_csv
    invalid_records = invalid_api + invalid_csv

    # 3. Save error report
    error_file = OUTPUT_DIR / "error_report.json"
    with open(error_file, "w", encoding="utf-8") as f:
        json.dump(invalid_records, f, indent=2, ensure_ascii=False)

    # 4. Database setup
    conn = get_connection()
    create_tables(conn)

    # 5. Insert RAW data (optional but now safer: only valid or full raw depending on design)
    insert_raw(conn, api_records, source="api")
    insert_raw(conn, csv_records, source="csv")

    # 6. Upsert ONLY valid records
    upsert_readings(conn, valid_records)

    # 7. Count final DB rows
    total_db_rows = count_readings(conn)

    # 8. Summary
    logger.info("=== Pipeline Summary ===")
    logger.info(f"API records fetched: {len(api_records)}")
    logger.info(f"CSV records read: {len(csv_records)}")
    logger.info(f"Total raw records: {len(api_records) + len(csv_records)}")
    logger.info(f"Valid records: {len(valid_records)}")
    logger.info(f"Invalid records: {len(invalid_records)}")
    logger.info(f"Records in database: {total_db_rows}")
    logger.info(f"Error report: {error_file}")


if __name__ == "__main__":
    run_pipeline()
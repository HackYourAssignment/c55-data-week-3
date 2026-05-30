# Step 6 — Task 6: Pipeline Orchestration
# This is the entry point. It calls every module you built in steps 1–5 in order.
# Implement run_pipeline() so that `python3 -m pipeline` produces a summary and
# writes output/error_report.json. The auto-grader runs this file directly.
import json
import logging
from pathlib import Path

from database import count_readings, create_tables, get_connection, insert_raw, upsert_readings
from ingest_api import fetch_api_records
from ingest_files import read_csv_records
from validate import validate_records

OUTPUT_DIR = Path("output")
CSV_PATH = Path("data/weather_stations.csv")


def run_pipeline() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    api_records = fetch_api_records()
    csv_records = read_csv_records(CSV_PATH)

    with get_connection() as conn:
        create_tables(conn)


        insert_raw(conn, api_records, "api")
        insert_raw(conn, csv_records, "csv")

        valid_api, error_api = validate_records(api_records, "api")
        valid_csv, error_csv = validate_records(csv_records, "csv")

        valid_records = valid_api + valid_csv
        error_records = error_api + error_csv

        upsert_readings(conn, valid_records)
        
        db_count = count_readings(conn)
    
    error_report_path = OUTPUT_DIR / "error_report.json"
    with error_report_path.open("w", encoding="utf-8") as f:
        json.dump(error_records, f, indent=2)
    print("=== Pipeline Summary ===")
    print(f"API records fetched: {len(api_records)}")
    print(f"CSV records read: {len(csv_records)}")
    print(f"Total raw records: {len(api_records) + len(csv_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(error_records)}")
    print(f"Records in database: {db_count}")
    print(f"Error report: {error_report_path}")


         


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()

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

    # TODO — implement each step in order:
    #
    # 1. Fetch records from Open-Meteo API using fetch_api_records()
    # 2. Read records from CSV using read_csv_records(CSV_PATH)
    # 3. Open a DB connection, create tables, insert all raw records (both sources)
    # 4. Validate all records — collect valid WeatherReading objects and error dicts
    # 5. Upsert valid records into weather_readings
    # 6. Save error dicts as JSON to output/error_report.json
    # 7. Print the pipeline summary in the format below.
    #
    # Note: the API count varies by time of day (Open-Meteo returns up to 168 hourly
    # records for 7 forecast days; the exact number depends on the current UTC hour).
    # The CSV contributes 6 invalid records and 4 valid ones; the duplicate Copenhagen
    # row is valid and exercises the upsert path rather than the validation error path.
    # Your actual output will look similar to this example:
    #
    #    === Pipeline Summary ===
    #    API records fetched: 166
    #    CSV records read: 10
    #    Total raw records: 176
    #    Valid records: 170
    #    Invalid records: 6
    #    Records in database: 169
    #    Error report: output/error_report.json

     # fetch API data
    api_records = fetch_api_records()

    # read CSV data
    csv_records = read_csv_records(CSV_PATH)

    # combine raw data
    all_raw_records = api_records + csv_records

    # DB setup
    conn = get_connection()
    create_tables(conn)

    # insert raw data
    insert_raw(conn, api_records, source="api")
    insert_raw(conn, csv_records, source="csv")

    # validate
    valid_api, invalid_api = validate_records(api_records, "api")

    # validate CSV
    valid_csv, invalid_csv = validate_records(csv_records, "csv")

# combine
    valid_records = valid_api + valid_csv
    invalid_records = invalid_api + invalid_csv

    # 7. Upsert valid records
    upsert_readings(conn, valid_records)

    # 8. Save error report
    error_path = OUTPUT_DIR / "error_report.json"
    with open(error_path, "w", encoding="utf-8") as f:
        json.dump(invalid_records, f, indent=2, ensure_ascii=False)

    # 9. Count final rows
    total_db_rows = count_readings(conn)

    # 10. Summary
    print("\n=== Pipeline Summary ===")
    print(f"API records fetched: {len(api_records)}")
    print(f"CSV records read: {len(csv_records)}")
    print(f"Total raw records: {len(all_raw_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(invalid_records)}")
    print(f"Records in database: {total_db_rows}")
    print(f"Error report: {error_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()

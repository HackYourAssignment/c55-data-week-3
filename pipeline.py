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

    # step 1 - fetch from API
    api_records = fetch_api_records()

    # step 2 - read from CSV
    csv_records = read_csv_records(CSV_PATH)

    # step 3 - combine both
    all_records = api_records + csv_records

    # step 4 - open database once
    conn = get_connection()
    create_tables(conn)

    # step 5 - insert all raw records
    insert_raw(conn, api_records, "api")
    insert_raw(conn, csv_records, "csv")
    conn.commit()

    # step 6 - validate all records
    valid_api, errors_api = validate_records(api_records, "api")
    valid_csv, errors_csv = validate_records(csv_records, "csv")
    valid = valid_api + valid_csv
    errors = errors_api + errors_csv

    # step 7 - upsert valid records
    upsert_readings(conn, valid)
    conn.commit()

    # step 8 - save error report
    error_report_path = OUTPUT_DIR / "error_report.json"
    with error_report_path.open("w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2, default=str)

    # step 9 - print summary
    print("=== Pipeline Summary ===")
    print(f"API records fetched: {len(api_records)}")
    print(f"CSV records read: {len(csv_records)}")
    print(f"Total raw records: {len(all_records)}")
    print(f"Valid records: {len(valid)}")
    print(f"Invalid records: {len(errors)}")
    print(f"Records in database: {count_readings(conn)}")
    print(f"Error report: {error_report_path}")

    conn.close()



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



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()

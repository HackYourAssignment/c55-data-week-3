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

    # 1. Fetch records from Open-Meteo API using fetch_api_records()
    api_records = fetch_api_records()
    
    # 2. Read records from CSV using read_csv_records(CSV_PATH)
    csv_records = read_csv_records(CSV_PATH)
    
    # 3. Open a DB connection, create tables, insert all raw records (both sources)
    conn = get_connection()
    create_tables(conn)

    insert_raw(conn, api_records, source="api")
    insert_raw(conn, csv_records, source="csv")    
    
    # 4. Validate all records — collect valid WeatherReading objects and error dicts
    all_records = api_records + csv_records

    valid_records, error_records = validate_records(
        all_records,
        source="csv",
    )    
    
    # 5. Upsert valid records into weather_readings
    upsert_readings(conn, valid_records)    
    
    # 6. Save error dicts as JSON to output/error_report.json
    error_report_path = OUTPUT_DIR / "error_report.json"

    with open(error_report_path, "w", encoding="utf-8") as file:
        json.dump(error_records, file, indent=2, ensure_ascii=False)    
    
    # 7. Print the pipeline summary in the format below.
    records_in_database = count_readings(conn)

    print("=== Pipeline Summary ===")
    print(f"API records fetched: {len(api_records)}")
    print(f"CSV records read: {len(csv_records)}")
    print(f"Total raw records: {len(all_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(error_records)}")
    print(f"Records in database: {records_in_database}")
    print(f"Error report: {error_report_path}")

    conn.close()    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()

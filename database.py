# Step 5 — Task 5: Database Storage
# create_tables()  — run once at startup to set up raw_weather and weather_readings.
# insert_raw()     — store every record before validation so nothing is lost.
# upsert_readings()— insert valid records; ON CONFLICT updates instead of duplicating.
# count_readings() — query the final row count for the pipeline summary.
import sqlite3
from pathlib import Path

from models import WeatherReading

DB_PATH = Path("weather.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn: sqlite3.Connection) -> None:

    conn.execute("""
    CREATE TABLE IF NOT EXISTS raw_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station TEXT,
        timestamp TEXT,
        temperature_c REAL,
        humidity_pct INTEGER,
        source TEXT,
        ingested_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS weather_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station TEXT,
        timestamp TEXT,
        temperature_c REAL,
        humidity_pct INTEGER,
        UNIQUE(station, timestamp)
    )
    """)

    conn.commit()


def insert_raw(conn: sqlite3.Connection, records: list[dict], source: str) -> None:

    for record in records:
        conn.execute("""
        INSERT INTO raw_weather (
            station,
            timestamp,
            temperature_c,
            humidity_pct,
            source
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            record.get("station"),
            record.get("timestamp"),
            record.get("temperature_c"),
            record.get("humidity_pct"),
            source
        ))

    conn.commit()


def upsert_readings(conn: sqlite3.Connection, readings: list[WeatherReading]) -> None:

    for r in readings:
        conn.execute("""
        INSERT INTO weather_readings (
            station,
            timestamp,
            temperature_c,
            humidity_pct
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(station, timestamp)
        DO UPDATE SET
            temperature_c = excluded.temperature_c,
            humidity_pct = excluded.humidity_pct
        """, (
            r.station,
            r.timestamp,
            r.temperature_c,
            r.humidity_pct
        ))

    conn.commit()


def count_readings(conn: sqlite3.Connection) -> int:

    cursor = conn.execute("""
    SELECT COUNT(*) as count FROM weather_readings
    """)

    return cursor.fetchone()["count"]
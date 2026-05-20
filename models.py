# Step 1 — Task 4: Pydantic Validation
# Define the WeatherReading model that every ingested record must pass.
# Both the API and CSV data flow through this model before reaching the database.
from pydantic import BaseModel, Field, field_validator, ValidationError


class WeatherReading(BaseModel):
    station: str = Field(..., min_length=1)
    timestamp: str = Field(..., min_length=1)
    temperature_c: float = Field(..., ge=-90, le=60)
    humidity_pct: int = Field(..., ge=0, le=100)

    @field_validator("station")
    @classmethod
    def clean_station(cls, v: str) -> str:
        # TODO: strip whitespace and convert to title case
        v = v.strip()
        v = v.title()
        return v

def validate_readings(raw_records: list[dict]) -> tuple[list[WeatherReading], list[dict]]:
    """Validate a list of raw records, returning valid records and errors."""
    valid = []
    errors = []

    for i, record in enumerate(raw_records):
        try:
            reading = WeatherReading(**record)
            valid.append(reading)
        except ValidationError as e:
            errors.append({
                "index": i,
                "record": record,
                "errors": e.errors(),
            })

    return valid, errors
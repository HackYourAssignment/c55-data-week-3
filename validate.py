# Step 4 — Task 4: Pydantic Validation (batch)
# validate_records() runs every record through WeatherReading and splits the
# results into a valid list and an error list. pipeline.py calls this once for
# all records combined, then stores the valid ones and saves the errors to JSON.
from pydantic import ValidationError

from models import WeatherReading


def validate_records(
    records: list[dict], source: str
) -> tuple[list[WeatherReading], list[dict]]:
    """Validate records against WeatherReading and return (valid_list, error_list).

    Each error dict must contain:
        index       - position of the record in the input list
        source      - the source string passed in (e.g. "api" or "csv")
        raw_record  - the original dict
        error_details - the Pydantic error list (ValidationError.errors())
    """
    # TODO: iterate over records, try WeatherReading(**record), accumulate results
    valid_records = []
    error_records = []
    for i, record in enumerate(records):
        try:
            validated_record = WeatherReading(**record)
            valid_records.append(validated_record)
        except ValidationError as e:
            error_records.append({
                "index": i,
                "source": source,
                "raw_record": record,
                "error_details": e.errors()
            })
    return valid_records, error_records 

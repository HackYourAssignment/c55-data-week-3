# AI Debugging Report

While building your pipeline you will run into at least one bug.
Document the debugging session below. If everything worked first try, introduce a bug intentionally and debug it.

---

## The Error

When I ran the pipeline with:
```bash
python pipeline.py

I got this traceback:
Traceback (most recent call last):
  File "G:\Halyna_work\traineeship_Amsterdam\Data-track\week-3\c55-data-week-3\pipeline.py", line 82, in <module>
    run_pipeline()
  File "G:\Halyna_work\traineeship_Amsterdam\Data-track\week-3\c55-data-week-3\pipeline.py", line 52, in run_pipeline
    api_valid, api_errors = validate_records(api_records, source="api")
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Halyna_work\traineeship_Amsterdam\Data-track\week-3\c55-data-week-3\validate.py", line 21, in validate_records
    raise NotImplementedError
NotImplementedError

The pipeline crashed during the validation step.

## The Prompt

I am working on a Week 3 data ingestion pipeline assignment.
When I run `python pipeline.py`, I get `NotImplementedError` from `validate.py`.

The traceback points to `validate_records(api_records, source="api")`.

How do I fix `validate_records` so it validates records with my Pydantic `WeatherReading` model, separates valid and invalid records, and returns both lists without crashing the pipeline?

## The Solution

The AI explained that raise NotImplementedError was only a placeholder.
It meant that the function existed, but the actual validation logic had not been implemented yet.

The suggested solution was to replace raise NotImplementedError with code that:

Creates an empty valid list.
Creates an empty errors list.
Loops over every raw record.
Tries to create a WeatherReading Pydantic model from the record.
Appends valid records to valid.
Catches ValidationError for invalid records.
Stores the index, source, raw data, and Pydantic error details in errors.
Returns (valid, errors).

The fixed function looked like this:

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

    valid: list[WeatherReading] = []
    errors: list[dict] = []

    for index, record in enumerate(records):
        try:
            valid.append(WeatherReading(**record))
        except ValidationError as exc:
            errors.append(
                {
                    "index": index,
                    "source": source,
                    "raw_record": record,
                    "error_details": exc.errors(),
                }
            )

    return valid, errors

After applying this fix, the pipeline no longer crashed at the validation step.
Instead, invalid records were collected into the error report.

## Reflection

I understand why the code was broken.
NotImplementedError means the function was still unfinished.
The pipeline expected validate_records to return two values: valid records and validation errors.
Instead, the function immediately raised an exception, so the pipeline stopped.

The fix works because Pydantic validates each record one by one.
Valid records continue through the pipeline and are written to the database.
Invalid records do not crash the pipeline; they are stored in the error list and later written to output/error_report.json.

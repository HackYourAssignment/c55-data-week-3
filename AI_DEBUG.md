# AI Debugging Report

While building your pipeline you will run into at least one bug.
Document the debugging session below. If everything worked first try, introduce a bug intentionally and debug it.

---

## The Error

When I tested `models.py`, I got this error:

```text
(.venv) pavel@Pavels-MacBook-Air c55-data-week-3 % python models.py
Traceback (most recent call last):
  File "/Users/pavel/Desktop/data _learn/c55-data-week-3/models.py", line 7, in <module>
    class WeatherReading(BaseModel):
  File "/Users/pavel/Desktop/data _learn/c55-data-week-3/models.py", line 28, in WeatherReading
    reading = WeatherReading(**good_record)
NameError: name 'WeatherReading' is not defined

The relevant code was:

class WeatherReading(BaseModel):
    station: str = Field(..., min_length=1)
    timestamp: str = Field(..., min_length=1)
    temperature_c: float = Field(..., ge=-90, le=60)
    humidity_pct: int = Field(..., ge=0, le=100)

    @field_validator("station", mode="before")
    @classmethod
    def clean_station(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().title()
        return v
    
    if __name__ == "__main__":
        good_record = {
            "station": " copenhagen ",
            "timestamp": "2025-01-15T10:00",
            "temperature_c": 18.5,
            "humidity_pct": 72,
        }

        reading = WeatherReading(**good_record)
        print(reading)

## The Prompt

I asked ChatGPT:

I get this error when I run python models.py:

Traceback (most recent call last):
  File "/Users/pavel/Desktop/data _learn/c55-data-week-3/models.py", line 7, in <module>
    class WeatherReading(BaseModel):
  File "/Users/pavel/Desktop/data _learn/c55-data-week-3/models.py", line 28, in WeatherReading
    reading = WeatherReading(**good_record)
NameError: name 'WeatherReading' is not defined

Here is my code. Why does Python say WeatherReading is not defined if I am defining the class in the same file?

## The Solution

ChatGPT explained that my test block was indented inside the WeatherReading class. Because of that, Python tried to run reading = WeatherReading(**good_record) while the class was still being created, so the class name did not exist yet.
The fix was to move this block to the left, outside the class:
if __name__ == "__main__":
    good_record = {
        "station": " copenhagen ",
        "timestamp": "2025-01-15T10:00",
        "temperature_c": 18.5,
        "humidity_pct": 72,
    }

    reading = WeatherReading(**good_record)
    print(reading)

After changing the indentation, the file worked and printed:

station='Copenhagen' timestamp='2025-01-15T10:00' temperature_c=18.5 humidity_pct=72

## Reflection

Before the AI answer, I did not really understand why the class was “not defined”, because visually it looked like I had already written the class. After the fix, I understood that Python indentation is not just style, it defines where the code belongs.

The bug happened because I placed test code inside the class by mistake. Next time I see a NameError inside a class body, I will check indentation first and make sure that temporary test code is outside the class or inside a separate test file.

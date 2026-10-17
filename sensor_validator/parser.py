import math
import re
from dataclasses import dataclass

_NUMBER_PATTERN = re.compile(r"[+-]?[0-9]+(?:\.[0-9]+)?")


class SensorFrameError(ValueError):
    """Raised when a sensor frame is malformed or contains invalid values."""


@dataclass(frozen=True)
class SensorReading:
    temperature_c: float
    humidity_percent: float


def parse_frame(frame: str) -> SensorReading:
    fields = frame.split(";")
    if len(fields) != 2:
        raise SensorFrameError("A frame must contain exactly TEMP and HUM fields")

    expected_keys = ("TEMP", "HUM")
    values = []
    for field, expected_key in zip(fields, expected_keys):
        key, separator, value = field.partition("=")
        if not separator or key.strip() != expected_key:
            raise SensorFrameError(f"Expected {expected_key} field")

        numeric_text = value.strip()
        if not _NUMBER_PATTERN.fullmatch(numeric_text):
            raise SensorFrameError(f"{expected_key} must use the documented number format")

        try:
            number = float(numeric_text)
        except ValueError as error:
            raise SensorFrameError(f"{expected_key} must be a number") from error

        if not math.isfinite(number):
            raise SensorFrameError(f"{expected_key} must be finite")
        values.append(number)

    temperature_c, humidity_percent = values
    if not -40 <= temperature_c <= 125:
        raise SensorFrameError("Temperature must be between -40 and 125 Celsius")
    if not 0 <= humidity_percent <= 100:
        raise SensorFrameError("Humidity must be between 0 and 100 percent")

    return SensorReading(temperature_c, humidity_percent)
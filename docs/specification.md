# Sensor Frame Validator Specification

## Input format

A frame contains exactly two fields in this order:

```text
TEMP=<number>;HUM=<number>
```

Temperature must come first, followed by humidity. Whitespace is allowed around fields, keys, and values. For example, ` TEMP = 21.5 ; HUM = 48 ` is valid.

## Numeric format

After surrounding whitespace is removed, each value must match this grammar:

```text
[+-]?[0-9]+(\.[0-9]+)?
```

The optional sign is an ASCII `+` or `-`. Digits are ASCII `0` through `9`. A decimal point, when present, must have at least one digit on both sides. Therefore, exponent notation, underscores, decimal commas, leading-dot decimals such as `.5`, and trailing-dot decimals such as `5.` are invalid.

## Value ranges

- Temperature is in Celsius and must be from -40 through 125, inclusive.
- Humidity is a percentage and must be from 0 through 100, inclusive.

## Errors and result

Reject frames with missing, duplicate, or extra fields; malformed numbers; NaN; infinity; or values outside the allowed ranges. Invalid frames raise `SensorFrameError`.

A valid frame returns a structured sensor reading containing its temperature and humidity values.
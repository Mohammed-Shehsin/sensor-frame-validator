# Test Matrix

| Category | Example frame or condition | Expected result | Test |
| --- | --- | --- | --- |
| Typical valid | `TEMP=21.5;HUM=48` | Reading: 21.5 C, 48% | `test_parse_normal_decimal_reading` |
| Integer and decimal values | `TEMP=20;HUM=48.5` | Reading: 20 C, 48.5% | `test_parse_integer_temperature_with_decimal_humidity` |
| Whitespace around fields | ` TEMP = 21.5 ; HUM = 48 ` | Reading: 21.5 C, 48% | `test_parse_frame_with_whitespace` |
| Whitespace around keys and values | Whitespace around either key or value | Reading: 21 C, 48% | `test_whitespace_around_keys_and_values_is_allowed` (parameterized) |
| Documented numeric forms | Optional ASCII sign, integer digits, and digits on both sides of optional decimal point in either field | Valid reading | `test_documented_numeric_forms_are_accepted_in_both_fields` (parameterized) |
| Disallowed numeric forms | Exponents, underscores, decimal commas, leading/trailing dots, sign without digits, or non-ASCII digits in either field | Raise `SensorFrameError` | `test_undocumented_numeric_forms_are_rejected_in_both_fields` (parameterized) |
| Minimum boundaries together | `TEMP=-40;HUM=0` | Valid reading | `test_lower_boundaries_are_accepted` |
| Each boundary independently | Temperature -40/125; humidity 0/100 with the other field in range | Valid reading | `test_each_range_boundary_is_accepted` (parameterized) |
| Just outside each range | Temperature -40.1/125.1; humidity -0.1/100.1 | Raise `SensorFrameError` | `test_values_outside_ranges_are_rejected` (parameterized) |
| Empty input or numeric value | Empty frame, `TEMP=;HUM=48`, `TEMP=21;HUM=` | Raise `SensorFrameError` | `test_empty_input_or_numeric_value_is_rejected` (parameterized) |
| Missing temperature | `HUM=48` | Raise `SensorFrameError` | `test_missing_temperature_is_rejected` |
| Missing humidity | `TEMP=21.5` | Raise `SensorFrameError` | `test_missing_humidity_raises_sensor_frame_error` |
| Duplicate fields | Duplicate TEMP or HUM keys | Raise `SensorFrameError` | `test_duplicate_fields_are_rejected` (parameterized) |
| Extra field | `TEMP=21;HUM=48;PRESS=101` | Raise `SensorFrameError` | `test_extra_field_is_rejected` |
| Reversed order | `HUM=48;TEMP=21` | Raise `SensorFrameError` | `test_reversed_field_order_is_rejected` |
| Incorrect field names | `TEM=21;HUM=48` or `TEMP=21;HUMID=48` | Raise `SensorFrameError` | `test_incorrect_field_names_are_rejected` (parameterized) |
| Missing or extra field separator | Missing `;` or doubled `;;` | Raise `SensorFrameError` | `test_missing_or_extra_field_separators_are_rejected` (parameterized) |
| Missing or extra equals signs | Missing `=` or doubled `==` in either field | Raise `SensorFrameError` | `test_missing_or_extra_equals_signs_are_rejected` (parameterized) |
| Non-numeric values | `TEMP=warm;HUM=48` or `TEMP=21;HUM=wet` | Raise `SensorFrameError` | `test_non_numeric_values_are_rejected` (parameterized) |
| NaN and both infinities | NaN, Infinity, or -Infinity in either field | Raise `SensorFrameError` | `test_non_finite_values_in_either_field_are_rejected` (parameterized) |

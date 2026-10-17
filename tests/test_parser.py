import pytest

from sensor_validator import SensorFrameError, SensorReading, parse_frame


def test_parse_normal_decimal_reading():
    assert parse_frame("TEMP=21.5;HUM=48.2") == SensorReading(21.5, 48.2)


def test_parse_integer_temperature_with_decimal_humidity():
    assert parse_frame("TEMP=20;HUM=48.5") == SensorReading(20.0, 48.5)


def test_parse_frame_with_whitespace():
    assert parse_frame(" TEMP = 21.5 ; HUM = 48 ") == SensorReading(21.5, 48.0)


def test_missing_humidity_raises_sensor_frame_error():
    with pytest.raises(SensorFrameError):
        parse_frame("TEMP=21.5")

def test_lower_boundaries_are_accepted():
    reading = parse_frame("TEMP=-40;HUM=0")
    assert reading == SensorReading(-40.0, 0.0)


@pytest.mark.parametrize(
    "frame, expected",
    [
        pytest.param("TEMP=-40;HUM=50", SensorReading(-40.0, 50.0), id="temperature-minimum"),
        pytest.param("TEMP=125;HUM=50", SensorReading(125.0, 50.0), id="temperature-maximum"),
        pytest.param("TEMP=20;HUM=0", SensorReading(20.0, 0.0), id="humidity-minimum"),
        pytest.param("TEMP=20;HUM=100", SensorReading(20.0, 100.0), id="humidity-maximum"),
    ],
)
def test_each_range_boundary_is_accepted(frame, expected):
    assert parse_frame(frame) == expected


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP=-40.1;HUM=50", id="temperature-below-minimum"),
        pytest.param("TEMP=125.1;HUM=50", id="temperature-above-maximum"),
        pytest.param("TEMP=20;HUM=-0.1", id="humidity-below-minimum"),
        pytest.param("TEMP=20;HUM=100.1", id="humidity-above-maximum"),
    ],
)
def test_values_outside_ranges_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("", id="empty-frame"),
        pytest.param("TEMP=;HUM=48", id="empty-temperature-value"),
        pytest.param("TEMP=21;HUM=", id="empty-humidity-value"),
    ],
)
def test_empty_input_or_numeric_value_is_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


def test_missing_temperature_is_rejected():
    with pytest.raises(SensorFrameError):
        parse_frame("HUM=48")


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP=20;TEMP=21", id="duplicate-temperature"),
        pytest.param("HUM=40;HUM=50", id="duplicate-humidity"),
    ],
)
def test_duplicate_fields_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


def test_extra_field_is_rejected():
    with pytest.raises(SensorFrameError):
        parse_frame("TEMP=21;HUM=48;PRESS=101")


def test_reversed_field_order_is_rejected():
    with pytest.raises(SensorFrameError):
        parse_frame("HUM=48;TEMP=21")


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEM=21;HUM=48", id="incorrect-temperature-key"),
        pytest.param("TEMP=21;HUMID=48", id="incorrect-humidity-key"),
    ],
)
def test_incorrect_field_names_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP=21 HUM=48", id="missing-field-separator"),
        pytest.param("TEMP=21;;HUM=48", id="extra-field-separator"),
    ],
)
def test_missing_or_extra_field_separators_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP21;HUM=48", id="missing-temperature-equals"),
        pytest.param("TEMP=21;HUM48", id="missing-humidity-equals"),
        pytest.param("TEMP==21;HUM=48", id="extra-temperature-equals"),
        pytest.param("TEMP=21;HUM==48", id="extra-humidity-equals"),
    ],
)
def test_missing_or_extra_equals_signs_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP=warm;HUM=48", id="non-numeric-temperature"),
        pytest.param("TEMP=21;HUM=wet", id="non-numeric-humidity"),
    ],
)
def test_non_numeric_values_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP=NaN;HUM=48", id="temperature-nan"),
        pytest.param("TEMP=Infinity;HUM=48", id="temperature-positive-infinity"),
        pytest.param("TEMP=-Infinity;HUM=48", id="temperature-negative-infinity"),
        pytest.param("TEMP=21;HUM=NaN", id="humidity-nan"),
        pytest.param("TEMP=21;HUM=Infinity", id="humidity-positive-infinity"),
        pytest.param("TEMP=21;HUM=-Infinity", id="humidity-negative-infinity"),
    ],
)
def test_non_finite_values_in_either_field_are_rejected(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param(" TEMP =21;HUM=48", id="temperature-key-whitespace"),
        pytest.param("TEMP=21; HUM =48", id="humidity-key-whitespace"),
        pytest.param("TEMP= 21 ;HUM=48", id="temperature-value-whitespace"),
        pytest.param("TEMP=21;HUM= 48 ", id="humidity-value-whitespace"),
    ],
)
def test_whitespace_around_keys_and_values_is_allowed(frame):
    assert parse_frame(frame) == SensorReading(21.0, 48.0)


@pytest.mark.parametrize(
    "frame, expected",
    [
        pytest.param("TEMP=+23;HUM=50", SensorReading(23.0, 50.0), id="temperature-plus-integer"),
        pytest.param("TEMP=-23;HUM=50", SensorReading(-23.0, 50.0), id="temperature-minus-integer"),
        pytest.param("TEMP=23.5;HUM=50", SensorReading(23.5, 50.0), id="temperature-decimal"),
        pytest.param("TEMP=+23.5;HUM=50", SensorReading(23.5, 50.0), id="temperature-plus-decimal"),
        pytest.param("TEMP=20;HUM=+48", SensorReading(20.0, 48.0), id="humidity-plus-integer"),
        pytest.param("TEMP=20;HUM=-0", SensorReading(20.0, 0.0), id="humidity-minus-zero"),
        pytest.param("TEMP=20;HUM=48.5", SensorReading(20.0, 48.5), id="humidity-decimal"),
        pytest.param("TEMP=20;HUM=+48.5", SensorReading(20.0, 48.5), id="humidity-plus-decimal"),
    ],
)
def test_documented_numeric_forms_are_accepted_in_both_fields(frame, expected):
    assert parse_frame(frame) == expected


@pytest.mark.parametrize(
    "frame",
    [
        pytest.param("TEMP=1e2;HUM=50", id="temperature-lowercase-exponent"),
        pytest.param("TEMP=1E2;HUM=50", id="temperature-uppercase-exponent"),
        pytest.param("TEMP=1_0;HUM=50", id="temperature-underscore"),
        pytest.param("TEMP=1,0;HUM=50", id="temperature-decimal-comma"),
        pytest.param("TEMP=.5;HUM=50", id="temperature-leading-dot"),
        pytest.param("TEMP=-.5;HUM=50", id="temperature-signed-leading-dot"),
        pytest.param("TEMP=+.5;HUM=50", id="temperature-plus-leading-dot"),
        pytest.param("TEMP=5.;HUM=50", id="temperature-trailing-dot"),
        pytest.param("TEMP=+;HUM=50", id="temperature-sign-without-digits"),
        pytest.param("TEMP=-;HUM=50", id="temperature-minus-without-digits"),
        pytest.param("TEMP=\u0661;HUM=50", id="temperature-non-ascii-digit"),
        pytest.param("TEMP=20;HUM=1e2", id="humidity-lowercase-exponent"),
        pytest.param("TEMP=20;HUM=1E2", id="humidity-uppercase-exponent"),
        pytest.param("TEMP=20;HUM=1_0", id="humidity-underscore"),
        pytest.param("TEMP=20;HUM=1,0", id="humidity-decimal-comma"),
        pytest.param("TEMP=20;HUM=.5", id="humidity-leading-dot"),
        pytest.param("TEMP=20;HUM=-.5", id="humidity-signed-leading-dot"),
        pytest.param("TEMP=20;HUM=+.5", id="humidity-plus-leading-dot"),
        pytest.param("TEMP=20;HUM=5.", id="humidity-trailing-dot"),
        pytest.param("TEMP=20;HUM=+", id="humidity-sign-without-digits"),
        pytest.param("TEMP=20;HUM=-", id="humidity-minus-without-digits"),
        pytest.param("TEMP=20;HUM=\u0661", id="humidity-non-ascii-digit"),
    ],
)
def test_undocumented_numeric_forms_are_rejected_in_both_fields(frame):
    with pytest.raises(SensorFrameError):
        parse_frame(frame)
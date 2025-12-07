"""Unit tests for utility functions.

This module verifies the correctness of the data transformation helpers
in app.core.utils, ensuring that numeric weather metrics are correctly
mapped to their descriptive text labels (e.g., Temperature -> "Cold").
"""

import pytest
from app.core.utils import get_temperature_label, get_humidity_label, get_wind_label


@pytest.mark.parametrize("temp, expected_label", [
    (-10.0, "Freezing"),
    (0.0, "Cold"),
    (4.9, "Cold"),
    (5.0, "Chilly"),
    (12.0, "Cool"),
    (15.0, "Warm"),
    (27.9, "Warm"),
    (28.0, "Hot"),
    (35.0, "Hot")
])
def test_get_temperature_label(temp, expected_label):
    """Verifies that temperatures map to the correct descriptive labels."""
    assert get_temperature_label(temp) == expected_label


@pytest.mark.parametrize("humidity, expected_label", [
    (25, "Dry"),
    (30, "Comfortable"),
    (50, "Comfortable"),
    (60, "Humid"),
    (80, "Humid")
])
def test_get_humidity_label(humidity, expected_label):
    """Verifies that humidity percentages map to the correct labels."""
    assert get_humidity_label(humidity) == expected_label


@pytest.mark.parametrize("speed, expected_label", [
    (0.0, "Calm"),
    (0.5, "Calm"),
    (1.0, "Light Breeze"),
    (5.0, "Gentle Breeze"),
    (20.0, "Strong Breeze"),
    (35.0, "Hurricane")
])
def test_get_wind_label(speed, expected_label):
    """Verifies that wind speeds map to the correct labels."""
    assert get_wind_label(speed) == expected_label
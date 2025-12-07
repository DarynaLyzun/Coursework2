"""Utility functions for the application.

This module contains helper functions for data transformation, such as
converting numeric weather metrics into descriptive text labels.
"""

def get_temperature_label(temp: float) -> str:
    """Converts a numeric temperature into a descriptive label based on user rules."""
    rules = [
        (0, "Freezing"),
        (5, "Cold"),
        (10, "Chilly"),
        (15, "Cool"),
        (28, "Warm"),
        (float('inf'), "Hot")
    ]
    
    for limit, label in rules:
        if temp < limit:
            return label
    return "Hot"

def get_humidity_label(humidity: int) -> str:
    """Converts humidity percentage into a descriptive label."""
    rules = [
        (30, "Dry"),
        (60, "Comfortable"),
        (float('inf'), "Humid")
    ]
    for limit, label in rules:
        if humidity < limit:
            return label
    return "Humid"

def get_wind_label(speed: float) -> str:
    """Converts wind speed (m/s) into a descriptive label (Beaufort scale)."""
    rules = [
        (1, "Calm"),
        (4, "Light Breeze"),
        (8, "Gentle Breeze"),
        (13, "Moderate Breeze"),
        (19, "Fresh Breeze"),
        (25, "Strong Breeze"),
        (33, "Storm"),
        (float('inf'), "Hurricane")
    ]
    
    for limit, label in rules:
        if speed < limit:
            return label
    return "Hurricane"
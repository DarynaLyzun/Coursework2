"""Utility functions for the application.

This module contains helper functions for data transformation, such as
converting numeric weather metrics into descriptive text labels.
"""

CANDIDATE_LABELS = [
    "Rain",
    "Cold",
    "Hot",
    "Windy",
    "Freezing",
    "Warm",
    "Sunny",
    "Snow",
    "Stormy",
    "Mild",
    "Cool"
]

def get_temperature_label(temp: float) -> str:
    """Converts a numeric temperature into a descriptive label based on user rules.

    Args:
        temp (float): The temperature in degrees Celsius.

    Returns:
        str: A text label (e.g., "Freezing", "Cool", "Hot").
    """
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
    """Converts humidity percentage into a descriptive label.

    Args:
        humidity (int): The humidity percentage (0-100).

    Returns:
        str: A text label (e.g., "Dry", "Comfortable", "Humid").
    """
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
    """Converts wind speed (m/s) into a descriptive label (Beaufort scale).

    Args:
        speed (float): The wind speed in meters per second.

    Returns:
        str: A text label (e.g., "Calm", "Gentle Breeze", "Storm").
    """
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
"""
Helper utilities for the Flask application.

Provides input validation and star-rating formatting helpers.
"""


def validate_prediction_input(form_data: dict) -> list:
    """
    Validate prediction form data and return a list of error messages.

    Parameters
    ----------
    form_data : dict
        Dictionary of form field values from the request.

    Returns
    -------
    list of str
        Empty list if all inputs are valid, otherwise a list of
        human-readable error messages.
    """
    errors = []

    # ── Required fields ──────────────────────────────────────────────────
    required_fields = [
        ("online_order", "Online Order"),
        ("book_table", "Book Table"),
        ("votes", "Votes"),
        ("cost", "Approx Cost for Two"),
        ("location", "Location"),
        ("rest_type", "Restaurant Type"),
        ("cuisines", "Cuisines"),
        ("type", "Type"),
        ("city", "City"),
    ]

    for field_key, field_label in required_fields:
        value = form_data.get(field_key, "").strip()
        if not value:
            errors.append(f"{field_label} is required.")

    if errors:
        return errors

    # ── Numeric validation ───────────────────────────────────────────────
    try:
        votes = int(form_data["votes"])
        if votes < 0:
            errors.append("Votes must be a non-negative integer.")
    except (ValueError, TypeError):
        errors.append("Votes must be a valid integer.")

    try:
        cost = float(form_data["cost"])
        if cost <= 0:
            errors.append("Approx Cost for Two must be a positive number.")
    except (ValueError, TypeError):
        errors.append("Approx Cost for Two must be a valid number.")

    return errors


def get_star_display(rating: float) -> dict:
    """
    Convert a numeric rating into display data for star rendering.

    Parameters
    ----------
    rating : float
        Rating between 1.0 and 5.0.

    Returns
    -------
    dict
        Keys:
          - rating      : float (the numeric rating)
          - full_stars   : int   (number of full stars)
          - half_star    : bool  (whether to show a half star)
          - empty_stars  : int   (number of empty stars)
          - percentage   : float (rating as percentage of 5)
    """
    full = int(rating)
    decimal = rating - full
    half = decimal >= 0.3
    empty = 5 - full - (1 if half else 0)

    return {
        "rating": rating,
        "full_stars": full,
        "half_star": half,
        "empty_stars": empty,
        "percentage": round((rating / 5) * 100, 1),
    }

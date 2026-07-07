"""
Predictor module for restaurant rating prediction.

Loads the trained Random Forest model and OrdinalEncoder once,
preprocesses input data, and returns predictions.
"""

import os
import json
import numpy as np
import joblib


# ── Paths ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(MODEL_DIR, "restaurant_rf_model.joblib")
ENCODER_PATH = os.path.join(MODEL_DIR, "categorical_encoder.joblib")
DROPDOWNS_PATH = os.path.join(MODEL_DIR, "ui_dropdowns.json")


# ── Singleton loader ─────────────────────────────────────────────────────
_model = None
_encoder = None
_dropdowns = None


def _load_model():
    """Load the Random Forest model (once)."""
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def _load_encoder():
    """Load the OrdinalEncoder (once)."""
    global _encoder
    if _encoder is None:
        _encoder = joblib.load(ENCODER_PATH)
    return _encoder


def load_dropdowns():
    """
    Load dropdown options from ui_dropdowns.json.

    Returns
    -------
    dict
        Keys: location, rest_type, cuisines, type, city
        Values: sorted list of string options
    """
    global _dropdowns
    if _dropdowns is None:
        with open(DROPDOWNS_PATH, "r", encoding="utf-8") as fh:
            _dropdowns = json.load(fh)
    return _dropdowns


def preprocess_and_predict(form_data: dict) -> float:
    """
    Preprocess user form data and return predicted rating.

    Expected form_data keys
    -----------------------
    online_order : str   ("Yes" / "No")
    book_table   : str   ("Yes" / "No")
    votes        : str   (integer string)
    cost         : str   (numeric string – approx cost for two)
    location     : str   (from dropdown)
    rest_type    : str   (from dropdown)
    cuisines     : str   (from dropdown)
    type         : str   (from dropdown)
    city         : str   (from dropdown)

    The model expects 9 features in the following order:
        online_order, book_table, votes, location, rest_type,
        cuisines, cost, type, city

    Categorical features (location, rest_type, cuisines, type, city)
    are encoded via the OrdinalEncoder that was fitted during training.
    online_order and book_table are mapped to 1/0.
    votes and cost are passed as numeric values.

    Returns
    -------
    float
        Predicted rating rounded to 1 decimal place, clamped to [1.0, 5.0].
    """
    model = _load_model()
    encoder = _load_encoder()

    # ── Binary features ─────────────────────────────────────────────────
    online_order = 1 if form_data.get("online_order", "No") == "Yes" else 0
    book_table = 1 if form_data.get("book_table", "No") == "Yes" else 0

    # ── Numeric features ────────────────────────────────────────────────
    votes = int(form_data.get("votes", 0))
    cost = float(form_data.get("cost", 0))

    # ── Categorical features ────────────────────────────────────────────
    # Encoder expects shape (1, 5) for columns:
    #   location, rest_type, cuisines, type, city
    cat_values = np.array([[
        form_data.get("location", ""),
        form_data.get("rest_type", ""),
        form_data.get("cuisines", ""),
        form_data.get("type", ""),
        form_data.get("city", ""),
    ]])

    cat_encoded = encoder.transform(cat_values)  # shape (1, 5)

    # ── Assemble feature vector ─────────────────────────────────────────
    # Model feature order:
    #   online_order, book_table, votes, location, rest_type,
    #   cuisines, cost, type, city
    features = np.array([[
        online_order,
        book_table,
        votes,
        cat_encoded[0, 0],   # location
        cat_encoded[0, 1],   # rest_type
        cat_encoded[0, 2],   # cuisines
        cost,
        cat_encoded[0, 3],   # type
        cat_encoded[0, 4],   # city
    ]])

    prediction = model.predict(features)[0]

    # Clamp between 1.0 and 5.0 and round
    prediction = round(float(np.clip(prediction, 1.0, 5.0)), 1)

    return prediction

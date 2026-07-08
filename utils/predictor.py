"""
Predictor module for restaurant rating prediction.

Loads the trained Random Forest model and OrdinalEncoder once,
validates inputs/dropdown schemas, preprocesses data, and outputs predictions.
"""

import json
import logging
import os
import threading
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor  # For type hinting
from sklearn.preprocessing import OrdinalEncoder  # For type hinting

logger = logging.getLogger(__name__)

# Constants
MIN_RATING: float = 1.0
MAX_RATING: float = 5.0
DECIMAL_PLACES: int = 1

# Features expected by model/encoder
CATEGORICAL_FEATURES: List[str] = [
    "location",
    "rest_type",
    "cuisines",
    "type",
    "city",
]

# Base paths calculation for fallback/standalone usages
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH: str = os.path.join(
    BASE_DIR, "model", "restaurant_rf_model.joblib"
)
DEFAULT_ENCODER_PATH: str = os.path.join(
    BASE_DIR, "model", "categorical_encoder.joblib"
)
DEFAULT_DROPDOWNS_PATH: str = os.path.join(
    BASE_DIR, "model", "ui_dropdowns.json"
)


def _get_config_path(key: str, default: str) -> str:
    """
    Retrieve filepath from current_app config or default if outside context.
    """
    try:
        from flask import current_app

        if current_app:
            return current_app.config[key]
    except (RuntimeError, KeyError):
        pass
    return os.environ.get(key, default)


def validate_dropdowns(data: Any) -> None:
    """
    Validate the schema structure of the dropdown options dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError("Dropdown data must be a dictionary.")

    for field in CATEGORICAL_FEATURES:
        if field not in data:
            raise ValueError(f"Missing required dropdown field: '{field}'")
        if not isinstance(data[field], list):
            raise TypeError(
                f"Dropdown field '{field}' must map to a list of options."
            )
        if not all(isinstance(item, str) for item in data[field]):
            raise ValueError(
                f"All options in '{field}' dropdown must be strings."
            )


class ModelLoader:
    """Thread-safe Singleton class loader for machine learning models and configurations."""

    _model: Optional[RandomForestRegressor] = None
    _encoder: Optional[OrdinalEncoder] = None
    _dropdowns: Optional[Dict[str, List[str]]] = None
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def load_model(cls, path: Optional[str] = None) -> RandomForestRegressor:
        if cls._model is None:
            with cls._lock:
                if cls._model is None:
                    target_path = path or _get_config_path(
                        "MODEL_PATH", DEFAULT_MODEL_PATH
                    )
                    logger.info("Loading ML Model from: %s", target_path)
                    try:
                        cls._model = joblib.load(target_path)
                    except Exception as exc:
                        logger.error(
                            "Failed to load ML Model from %s: %s",
                            target_path,
                            exc,
                        )
                        raise
        return cls._model

    @classmethod
    def load_encoder(cls, path: Optional[str] = None) -> OrdinalEncoder:
        if cls._encoder is None:
            with cls._lock:
                if cls._encoder is None:
                    target_path = path or _get_config_path(
                        "ENCODER_PATH", DEFAULT_ENCODER_PATH
                    )
                    logger.info("Loading Ordinal Encoder from: %s", target_path)
                    try:
                        cls._encoder = joblib.load(target_path)
                    except Exception as exc:
                        logger.error(
                            "Failed to load Encoder from %s: %s",
                            target_path,
                            exc,
                        )
                        raise
        return cls._encoder

    @classmethod
    def load_dropdowns(cls, path: Optional[str] = None) -> Dict[str, List[str]]:
        if cls._dropdowns is None:
            with cls._lock:
                if cls._dropdowns is None:
                    target_path = path or _get_config_path(
                        "DROPDOWNS_PATH", DEFAULT_DROPDOWNS_PATH
                    )
                    logger.info(
                        "Loading and validating dropdowns from: %s",
                        target_path,
                    )
                    try:
                        with open(target_path, "r", encoding="utf-8") as fh:
                            data = json.load(fh)
                        validate_dropdowns(data)
                        cls._dropdowns = data
                    except Exception as exc:
                        logger.error(
                            "Failed to load/validate dropdown options from %s: %s",
                            target_path,
                            exc,
                        )
                        raise
        return cls._dropdowns


# ── Module-Level Wrapper Functions for External Imports ─────────────────

def load_dropdowns(path: Optional[str] = None) -> Dict[str, List[str]]:
    """Exposes dropdown loading to app.py at the module level."""
    return ModelLoader.load_dropdowns(path)


def preprocess_and_predict(form_data: Dict[str, str]) -> float:
    """
    Preprocess user form data, encode categorical variables, and return predictions.
    """
    model = ModelLoader.load_model()
    encoder = ModelLoader.load_encoder()

    # Binary features mapping
    online_order: int = (
        1 if form_data.get("online_order", "No") == "Yes" else 0
    )
    book_table: int = 1 if form_data.get("book_table", "No") == "Yes" else 0

    # Safe Numeric Conversion
    votes: int = 0
    raw_votes = form_data.get("votes", "0")
    try:
        votes = int(raw_votes)
    except (ValueError, TypeError) as exc:
        logger.warning(
            "Numeric parsing failure for 'votes' value: %s. Defaulting to 0. Error: %s",
            raw_votes,
            exc,
        )

    cost: float = 0.0
    raw_cost = form_data.get("cost", "0.0")
    try:
        cost = float(raw_cost)
    except (ValueError, TypeError) as exc:
        logger.warning(
            "Numeric parsing failure for 'cost' value: %s. Defaulting to 0.0. Error: %s",
            raw_cost,
            exc,
        )

    # Categorical features
    cat_values = np.array(
        [
            [
                form_data.get("location", ""),
                form_data.get("rest_type", ""),
                form_data.get("cuisines", ""),
                form_data.get("type", ""),
                form_data.get("city", ""),
            ]
        ]
    )

    try:
        cat_encoded = encoder.transform(cat_values)
    except Exception as exc:
        logger.error(
            "Encoding failed for categorical values: %s. Error: %s",
            cat_values,
            exc,
        )
        raise

    # Assemble feature vector
    features = np.array(
        [
            [
                online_order,
                book_table,
                votes,
                cat_encoded[0, 0],  # location
                cat_encoded[0, 1],  # rest_type
                cat_encoded[0, 2],  # cuisines
                cost,
                cat_encoded[0, 3],  # type
                cat_encoded[0, 4],  # city
            ]
        ]
    )

    # Run Prediction
    raw_prediction = model.predict(features)[0]

    # Clamp and round predicted score
    prediction = round(
        float(np.clip(raw_prediction, MIN_RATING, MAX_RATING)),
        DECIMAL_PLACES,
    )

    return prediction


# ── Backwards Compatibility Aliases for Legacy app.py Imports ───────────

def _load_model(path: Optional[str] = None) -> RandomForestRegressor:
    """Alias pointing to the thread-safe ModelLoader to satisfy app.py."""
    return ModelLoader.load_model(path)


def _load_encoder(path: Optional[str] = None) -> OrdinalEncoder:
    """Alias pointing to the thread-safe ModelLoader to satisfy app.py."""
    return ModelLoader.load_encoder(path)

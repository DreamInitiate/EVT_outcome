"""Locked implementation of the post-EVT logistic regression model."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Mapping


MODEL_PATH = Path(__file__).resolve().parent / "model" / "model.json"


def load_model() -> dict:
    """Load the authoritative machine-readable model specification."""
    with MODEL_PATH.open(encoding="utf-8") as model_file:
        return json.load(model_file)


MODEL = load_model()
PREDICTOR_IDS = tuple(item["id"] for item in MODEL["predictors"])


def predict(values: Mapping[str, float | int]) -> tuple[float, float]:
    """Return (linear predictor, probability) for one complete input record."""
    missing = [predictor_id for predictor_id in PREDICTOR_IDS if predictor_id not in values]
    if missing:
        raise ValueError(f"Missing predictors: {', '.join(missing)}")

    linear_predictor = float(MODEL["intercept"])
    for predictor in MODEL["predictors"]:
        value = float(values[predictor["id"]])
        if not math.isfinite(value):
            raise ValueError(f"{predictor['id']} must be finite")
        if predictor["type"] == "binary" and value not in (0.0, 1.0):
            raise ValueError(f"{predictor['id']} must be coded 0 or 1")
        linear_predictor += float(predictor["coefficient"]) * value

    probability = 1.0 / (1.0 + math.exp(-linear_predictor))
    return linear_predictor, probability


def validate_plausibility(values: Mapping[str, float | int]) -> list[str]:
    """Apply broad UI guardrails; these are not training-cohort ranges."""
    errors: list[str] = []
    for predictor in MODEL["predictors"]:
        predictor_id = predictor["id"]
        if predictor_id not in values:
            errors.append(f"{predictor['label']} is required.")
            continue
        value = values[predictor_id]
        if value is None:
            errors.append(f"{predictor['label']} is required.")
            continue
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            errors.append(f"{predictor['label']} must be numeric.")
            continue
        if not math.isfinite(numeric_value):
            errors.append(f"{predictor['label']} must be finite.")
        elif predictor["type"] == "binary" and numeric_value not in (0.0, 1.0):
            errors.append(f"{predictor['label']} must be No (0) or Yes (1).")
        elif predictor["type"] == "continuous" and not (
            float(predictor["ui_min"]) <= numeric_value <= float(predictor["ui_max"])
        ):
            errors.append(
                f"{predictor['label']} must be between "
                f"{predictor['ui_min']} and {predictor['ui_max']} {predictor['unit']}."
            )
    return errors

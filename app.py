"""
Flask application for Bengaluru Restaurant Rating Predictor.

Routes
------
/          – Home page
/predict   – GET: prediction form  |  POST: run prediction → result
/about     – About the project

Custom error handlers for 404 and 500.
"""

from flask import Flask, render_template, request, redirect, url_for, flash

from utils.predictor import load_dropdowns, preprocess_and_predict
from utils.helper import validate_prediction_input, get_star_display


# ── App factory ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "bengaluru-restaurant-rating-predictor-2024"


# ── Routes ───────────────────────────────────────────────────────────────

@app.route("/")
def home():
    """Render the landing / home page."""
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    GET  → Render prediction form with dropdown values.
    POST → Validate input, run prediction, show result page.
    """
    dropdowns = load_dropdowns()

    if request.method == "GET":
        return render_template("predict.html", dropdowns=dropdowns)

    # ── POST: collect form data ──────────────────────────────────────
    form_data = {
        "online_order": request.form.get("online_order", "").strip(),
        "book_table": request.form.get("book_table", "").strip(),
        "votes": request.form.get("votes", "").strip(),
        "cost": request.form.get("cost", "").strip(),
        "location": request.form.get("location", "").strip(),
        "rest_type": request.form.get("rest_type", "").strip(),
        "cuisines": request.form.get("cuisines", "").strip(),
        "type": request.form.get("type", "").strip(),
        "city": request.form.get("city", "").strip(),
    }

    # ── Validate ─────────────────────────────────────────────────────
    errors = validate_prediction_input(form_data)
    if errors:
        for err in errors:
            flash(err, "error")
        return render_template(
            "predict.html", dropdowns=dropdowns, form_data=form_data
        )

    # ── Predict ──────────────────────────────────────────────────────
    try:
        rating = preprocess_and_predict(form_data)
        star_data = get_star_display(rating)
        return render_template(
            "result.html",
            star_data=star_data,
            form_data=form_data,
        )
    except Exception as exc:
        flash(f"Prediction failed: {exc}", "error")
        return render_template(
            "predict.html", dropdowns=dropdowns, form_data=form_data
        )


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


# ── Error handlers ───────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 page."""
    return render_template("404.html", error_code=500,
                           error_message="Internal Server Error"), 500


# ── Entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Pre-load model and encoder on startup
    from utils.predictor import _load_model, _load_encoder
    print("Loading model and encoder...")
    _load_model()
    _load_encoder()
    load_dropdowns()
    print("Ready!")
    app.run(debug=True, host="0.0.0.0", port=5000)

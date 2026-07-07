# Bengaluru Restaurant Rating Predictor 🍽️

A full-stack Flask web application powered by Machine Learning that predicts the Zomato rating of a restaurant in Bengaluru based on various features.

## 📌 Project Overview
This project leverages a pre-trained **Random Forest Regression** model to predict restaurant ratings. The model was trained on a dataset of 50,000+ Bengaluru restaurants from Zomato. The Flask backend takes input from a modern, responsive UI designed with HTML5, CSS3, and JavaScript, preprocesses it to match the exact training pipeline format, and instantly outputs the predicted rating out of 5.

## ✨ Features
- **Instant Rating Predictions**: Receive accurate ratings out of 5 based on key restaurant metrics. 
- **Machine Learning Powered**: Uses an ensemble `RandomForestRegressor` and categorical `OrdinalEncoder`.
- **Dynamic Dropdowns**: Loads location, cuisine, type, and city options directly from JSON.
- **Beautiful UI/UX**: Custom-designed responsive interface inspired by modern food delivery apps (Zomato-themed), with CSS glassmorphism, smooth animations, and zero dependency on external CSS frameworks like Bootstrap.
- **Form Validation**: Strict client-side and server-side validation.

## 📂 Folder Structure
```
restaurant-rating-predictor/
├── app.py                     # Main Flask application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation (this file)
├── .gitignore                 # Files ignored by Git
│
├── model/                     # ML Model and Encoders (Do Not Modify)
│   ├── restaurant_rf_model.joblib
│   ├── categorical_encoder.joblib
│   └── ui_dropdowns.json
│
├── static/                    # Frontend static assets
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── script.js          # Interactive scripts
│   ├── images/
│   └── icons/
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layouts (navbar, footer)
│   ├── index.html             # Landing/Home page
│   ├── predict.html           # Rating prediction form
│   ├── result.html            # Rating prediction result
│   ├── about.html             # About the project & models
│   └── 404.html               # Custom 404 Error page
│
└── utils/                     # Python logic utilities
    ├── __init__.py
    ├── predictor.py           # Loads model and handles predictions
    └── helper.py              # Validation and result formatting helpers
```

## 🚀 Installation & Setup

1. **Clone the repository** (if hosted on GitHub):
   ```bash
   git clone https://github.com/yourusername/restaurant-rating-predictor.git
   cd restaurant-rating-predictor
   ```

2. **Create a virtual environment (Recommended)**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ How to Run

1. Ensure your virtual environment is activated.
2. Run the application from the root folder:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📸 Screenshots
*(Replace these placeholders with actual screenshots of the application)*

- **Home Page**: `![Home Page](placeholder.jpg)`
- **Prediction Form**: `![Form](placeholder.jpg)`
- **Results Card**: `![Results](placeholder.jpg)`

## 🔮 Future Improvements
- Add a map integration to select actual latitude and longitude points.
- Fine-tune a model utilizing Deep Learning (e.g., neural networks).
- Dockerize the application for easier deployment.
- Integrate real-time API data to track changing trends.

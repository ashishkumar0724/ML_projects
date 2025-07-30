# classifier.py
import joblib
import html
import pandas as pd
import os
import numpy as np

# --- Model Management ---
MODEL_DIR = "models"
AVAILABLE_MODELS = {
    "Hybrid Ensemble Model": "spam_hybrid_ensemble_model.pkl",
    "Linear SVM Model": "spam_tuned_linear_svm_model.pkl",
    "Logistic Regression Model": "spam_tuned_logistic_regression_model.pkl",
}

def load_model(model_filename):
    """Load a specific model by filename"""
    try:
        model_path = os.path.join(MODEL_DIR, model_filename)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_filename}' not found in {MODEL_DIR}")
        model = joblib.load(model_path)
        # Check for required methods
        if not (hasattr(model, 'predict_proba') or hasattr(model, 'decision_function') or hasattr(model, 'predict')):
             raise AttributeError(f"Model {model_filename} doesn't support required prediction methods.")
        return model
    except Exception as e:
        raise e # Re-raise for the caller to handle

# --- Preprocessing Function ---
def clean_text(text):
    """Must match exactly what was used during training"""
    if pd.isna(text):  # Handle NaN values
        return ""
    text = html.unescape(text)  # Handle HTML escape chars like &amp;
    text = text.lower()
    text = ' '.join(text.split())  # Normalize whitespace
    return text

# --- Prediction Function ---
def get_prediction_and_probability(model, cleaned_input):
    """Handle prediction for different model types"""
    try:
        # Get prediction
        prediction = model.predict([cleaned_input])[0] # Pass as list
        # Try to get probability
        if hasattr(model, 'predict_proba'):
            probability_spam = model.predict_proba([cleaned_input])[0][1]
            return prediction, probability_spam, True
        elif hasattr(model, 'decision_function'):
            # For SVM, decision function gives distance from hyperplane
            decision_score = model.decision_function([cleaned_input])[0]
            # Convert to pseudo-probability using sigmoid
            probability_spam = 1 / (1 + np.exp(-decision_score))
            # Normalize to 0-1 range if needed
            probability_spam = max(0, min(1, probability_spam))
            return prediction, probability_spam, False
        else:
            # Fallback - no probability available
            return prediction, 0.5, False
    except Exception as e:
        raise e # Re-raise for the caller to handle

# --- Helper to get model filename from display name ---
def get_model_filename(display_name):
    return AVAILABLE_MODELS.get(display_name)
import os
import pandas as pd
from src.utils import load_object  # Assuming you have a utility to load objects
import pickle

# Paths to model and preprocessor
model_path = os.path.join("artifacts", "model.pkl")
preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")

# Load the model and preprocessor
def load_model_and_preprocessor(model_path, preprocessor_path):
    try:
        # Load preprocessor
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)
        # Load model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        print("Model and preprocessor loaded successfully.")
        return model, preprocessor
    except Exception as e:
        print(f"Error loading model/preprocessor: {e}")
        return None, None

# Create sample input data
def create_sample_data():
    data = {
        "Age": [50],             # Example Age
        "Sex": ["male"],         # Example Sex
        "BP": ["low"],          # Example Blood Pressure
        "Cholesterol": ["high"], # Example Cholesterol
        "Na_to_K": [15.5]        # Example Sodium to Potassium Ratio
    }
    return pd.DataFrame(data)

# Test the model and preprocessor with sample data
def test_model(model, preprocessor, sample_data):
    try:
        # Preprocess the data
        print("Original Sample Data:")
        print(sample_data)

        processed_data = preprocessor.transform(sample_data)
        print("Transformed Data:")
        print(processed_data)

        # Make predictions
        predictions = model.predict(processed_data)
        print("Prediction Result:")
        print(predictions)
    except Exception as e:
        print(f"Error during prediction: {e}")

if __name__ == "__main__":
    # Load model and preprocessor
    model, preprocessor = load_model_and_preprocessor(model_path, preprocessor_path)

    if model and preprocessor:
        # Create sample data
        sample_data = create_sample_data()

        # Test the model with the sample data
        test_model(model, preprocessor, sample_data)

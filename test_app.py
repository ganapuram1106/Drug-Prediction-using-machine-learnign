import pytest
from unittest.mock import patch
from app import app  # Adjust the import path to your Flask app

@pytest.fixture
def client():
    """Fixture to create a Flask test client."""
    with app.test_client() as client:
        yield client

@patch('src.pipeline.predict_pipeline.PredictPipeline.predict')
def test_predict_post(mock_predict, client):
    """Test the /predictdata page (POST request) with form data."""
    
    # Mock the prediction output
    mock_predict.return_value = ["drugY"]  # Replace with the expected prediction result

    form_data = {
        'age': '30',
        'sex': 'Male',
        'bp': 'High',
        'cholesterol': 'Normal',
        'na_to_k': '15.5'
    }

    # Send POST request to /predictdata, allowing redirects
    response = client.post('/predictdata', data=form_data, follow_redirects=True)
    
    # Assert the status code is 200 OK
    assert response.status_code == 200

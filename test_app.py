from unittest.mock import patch
import pytest
from app import app

@pytest.fixture
def client():
    # Setup: configure app for testing
    app.config['TESTING'] = True
    client = app.test_client()
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

    # Send POST request to /predictdata
    response = client.post('/predictdata', data=form_data)
    
    # Assert the status code is 200 OK
    assert response.status_code == 200
    
    # Assert that the predicted value "drugY" is present in the response data
    assert b"drugY" in response.data
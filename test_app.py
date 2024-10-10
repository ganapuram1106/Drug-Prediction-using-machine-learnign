from app import app
import pytest

@pytest.fixture
def client():
    
    app.config['TESTING'] = True  
    client = app.test_client()     
    yield client                   


def test_home_page(client):
    
    response = client.get('/')  
    assert response.status_code == 200  
    assert b"Home" in response.data     


def test_predict_get(client):
    
    response = client.get('/predictdata')  
    assert response.status_code == 200     
    assert b"Prediction" in response.data  

def test_predict_post(client):
    
    form_data = {
        'age': '30',
        'sex': 'Male',
        'bp': 'High',
        'cholesterol': 'Normal',
        'na_to_k': '15.5'
    }
    response = client.post('/predictdata', data=form_data) 
    assert response.status_code == 200                      
    assert b"Results" in response.data 


def test_404_page(client):
    """Test a non-existing page (404 error)"""
    response = client.get('/nonexistentpage')  
    assert response.status_code == 404         
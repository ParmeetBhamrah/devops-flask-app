import pytest
from app import app

@pytest.fixture
def client():
    # Configure app for testing mode
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Health endpoint must always return 200 and healthy status"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_home_page(client):
    """Home page must return 200"""
    response = client.get('/')
    assert response.status_code == 200
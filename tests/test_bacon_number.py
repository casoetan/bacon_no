from bacon_number.api import app
from fastapi.testclient import TestClient

"""This is a basic test using the dataset imported

Normally we should create a mock database to test against
"""

client = TestClient(app)

def test_get_actors():
    response = client.get('/actors/Pierce')
    assert response.status_code == 200
    content = response.json()
    assert 'actors' in content
    assert 'name' in content['actors'][0]
    assert 'Pierce' in content['actors'][0]['name']
    assert len(content['actors']) <= 10

def test_get_non_existent_actors():
    response = client.get('/actors/XYZXX')
    assert response.status_code == 404
    content = response.json()
    assert content['detail'] == 'Actor not found'

def test_get_bacon_number():
    response = client.get('/degrees/31')
    assert response.status_code == 200
    content = response.json()
    assert 'degree_no' in content
    assert 'info' in content
    assert content['degree_no'] == 2
    assert 'Kevin Bacon' in content['info']
    assert 'Tom Hanks' in content['info']

def test_get_degrees_number():
    response = client.get('/degrees/517?degrees_to=31')
    assert response.status_code == 200
    content = response.json()
    assert 'degree_no' in content
    assert 'info' in content
    assert content['degree_no'] == 3
    assert 'Pierce Brosnan' in content['info']
    assert 'Tom Hanks' in content['info']

def test_get_bacon_number_for_invalid_actor_id():
    response = client.get('/degrees/51787')
    assert response.status_code == 404
    content = response.json()
    assert content['detail'] == 'One or both of actors do not exist'

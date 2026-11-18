import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint returns a welcome message."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'Welcome' in data['message']

def test_get_tasks_empty(client):
    """Test GET /todos returns an empty list initially."""
    response = client.get('/todos')
    assert response.status_code == 200
    data = response.get_json()
    assert 'tasks' in data
    assert isinstance(data['tasks'], list)

def test_create_task_valid(client):
    """Test POST /todos creates a new task with valid data."""
    response = client.post('/todos', json={
        'title': 'Learn DevOps',
        'description': 'Study Flask CI/CD pipeline'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'task' in data
    assert data['task']['title'] == 'Learn DevOps'
    assert data['task']['description'] == 'Study Flask CI/CD pipeline'
    assert 'id' in data['task']
    assert 'created_at' in data['task']

def test_create_task_invalid_missing_title(client):
    """Test POST /todos with missing title returns 400."""
    response = client.post('/todos', json={
        'description': 'Missing title'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_create_task_invalid_missing_description(client):
    """Test POST /todos with missing description returns 400."""
    response = client.post('/todos', json={
        'title': 'Test task'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_create_task_invalid_no_json(client):
    """Test POST /todos with no JSON body returns 400."""
    response = client.post('/todos', data='', content_type='text/plain')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_health_endpoint(client):
    """Test the health endpoint returns healthy status."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

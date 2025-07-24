import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['FLASK_ENV'] = 'testing'

from app import app, db, Todo

@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()

def test_delete_action(client):

    client.post('/login', data={
        'username': 'haris_00',
        'password': '1010'
    }, follow_redirects=True)


    client.post('/', data={
        'title': 'Delete',
        'desc': 'Testing delete'
    }, follow_redirects=True)

    from app import Todo
    todo = Todo.query.filter_by(title='Delete').first()
    assert todo is not None


    response = client.get(f'/delete/{todo.sno}', follow_redirects=True)
    assert response.status_code == 200

def test_signup(client):
    response = client.get('/signup', follow_redirects=True)
    assert response.status_code == 200

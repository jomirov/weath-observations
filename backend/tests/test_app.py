from fastapi.testclient import TestClient
from ..dependencies import get_path
from ..app import app

def temp_path():
    return "tests/test.db"

client = TestClient(app)

app.dependency_overrides[get_path] = lambda: "tests/test.db"

def test_temp_db():
    assert client.get('/observations', headers={"x-token": "TOKEN-A"})
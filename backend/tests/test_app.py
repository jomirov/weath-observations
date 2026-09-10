from fastapi.testclient import TestClient
from ..dependencies import get_path
from ..app import app
from ..database.db import Sqlite3db
from dotenv import load_dotenv
import pytest
from pathlib import Path

load_dotenv(".env.example")

client = TestClient(app)

def temp_path():
    return "../backend/tests/test.db"

@pytest.fixture(autouse=True)
def db():
    app.dependency_overrides[get_path] = temp_path
sqlite3db = Sqlite3db(temp_path())
con = sqlite3db.connect()
cur = con.cursor()

def test_insert_valid_observation():
    res = client.post('/observations', 
                       headers={"x-token": "TEST-TOKEN-A"}, 
                       json={
                           "city" : "Almaty",
                           "temperature_C": 12,
                           "note": "Rainy"
                       })

    cur.execute("SELECT MAX(id) FROM observations")
    new_observation_id = cur.fetchone()[0]
    cur.execute("SELECT owner_id FROM observations WHERE id = ?", (new_observation_id,))
    user_id = cur.fetchone()[0]

    assert res.status_code == 201
    assert res.json() == {"status": "OK", "message": f"Observation by {new_observation_id} ID has been created"}
    assert user_id == 1

def test_insert_invalid_observation():
    base_count = cur.execute("SELECT COUNT(*) FROM observations").fetchone()[0]

    res = client.post('/observations', 
                      headers={"x-token": "TEST-TOKEN-A"}, 
                      json={"city":" ",
                            "temperature_C": 20
                      })
    assert res.status_code == 422

    res = client.post('/observations',
                      headers={"x-token":"TEST-TOKEN-A"},
                      json={"city": "Almaty",
                            "temperature_C": 100
                      })
    assert res.status_code == 422

    assert base_count == cur.execute("SELECT COUNT(*) FROM observations").fetchone()[0]

def test_unauthorized_user():
    res = client.get('/observations', headers={"x-token":"invalid-token"})

    assert res.status_code == 401

def test_access_data_user1_from_user2():
    res = client.get('/observations', headers={"x-token":"TEST-TOKEN-B"})

    user2_observations = res.json()
    contains_user1_observation = False
    for o in user2_observations:
        if o["owner_id"] == 1:
            contains_user1_observation = True

    assert contains_user1_observation == False

    cur.execute("SELECT MAX(id) FROM observations WHERE owner_id = 1")
    user1_last_observation_id = cur.fetchone()[0]

    res = client.get(f'/observations/{user1_last_observation_id}', headers={"x-token": "TEST-TOKEN-B"})
    assert res.status_code == 404

    res = client.delete(f'/observations/{user1_last_observation_id}', headers={"x-token": "TEST-TOKEN-B"})
    assert res.status_code == 404
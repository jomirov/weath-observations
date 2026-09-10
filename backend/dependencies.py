import os
from fastapi import Depends
from dotenv import load_dotenv
from .database.observation import Observation
from .database.observationDAO import ObservationDAO
from .database.db import Sqlite3db

load_dotenv()


def get_path():
    return os.getenv("DB_path")

def get_obs_dao(db_path: str = Depends(get_path)):
    return ObservationDAO(Sqlite3db(db_path=db_path))

def identify_user(x_token):
    if os.getenv(x_token) != None:
        return int(os.getenv(x_token))
    return -1

def is_valid_observation(o: Observation):
    city = o.city.strip()
    temp = o.temperature_C
    note = o.note.strip() if o.note != None else None
    if len(city) > 80 or len(city) < 1:
        return False
    elif temp < -90 or temp > 60:
        return False
    elif note != None and len(note) > 300:
        return False
    return True

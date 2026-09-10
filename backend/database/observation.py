from pydantic import BaseModel

class Observation(BaseModel):
    city: str
    temperature_C: int
    note: str | None = None
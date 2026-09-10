from .db import Sqlite3db

class ObservationDAO:
    def __init__(self, db: Sqlite3db):
        self.db = db
        self.con = self.db.connect()
        self.cur = self.con.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS observations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
                city VARCHAR(80),
                temperature_C INTEGER,
                note VARCHAR(300)
            )
        """)
        self.con.commit()
    
    #crud
    def insert_observation(self, owner_id: int, 
                        city: str, 
                        temperature_C: int, 
                        note: str):
        self.cur.execute(
            "INSERT INTO observations (owner_id, city, temperature_C, note) values (?, ?, ?, ?)",
            (owner_id, city, temperature_C, note)
        )
        self.cur.execute("SELECT MAX(id) FROM observations")
        self.con.commit()
        return self.cur.fetchone()[0]

    def get_observations(self,owner_id: int):
        self.cur.execute("SELECT * FROM observations WHERE owner_id = ?", (owner_id,))
        res = self.cur.fetchall()
        data = []
        for o in res:
            data.append({
                "id": o[0],
                "owner_id": o[1],
                "city": o[2],
                "temperature_C": o[3],
                "note": o[4]
            })
        return data

    def get_observation_by_id(self,id: int):
        self.cur.execute("SELECT * FROM observations WHERE id = ?", (id,))
        res = self.cur.fetchone()
        
        data = {
            "id": int(res[0]),
            "owner_id": int(res[1]),
            "city": res[2],
            "temperature_C": int(res[3]),
            "note": res[4]
        } if res != None else None
        return data

    def delete_observation_by_id(self,id:int):
        self.cur.execute("DELETE FROM observations WHERE id = ?", (id,))
        self.con.commit()
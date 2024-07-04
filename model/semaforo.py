from utils.db import db
from dataclasses import dataclass

@dataclass
class Semaforo(db.Model):
    __tablename__='semaforo'
    id: int
    color: str
    
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50))
    
    def __init__(self, color):
        self.color = color
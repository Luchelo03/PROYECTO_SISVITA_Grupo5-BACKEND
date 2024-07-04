from utils.db import db
from dataclasses import dataclass

@dataclass
class Departamentos(db.Model):
    __tablename__ = 'department'
    id: int
    ubigeo: str
    department: str
    
    id = db.Column(db.Integer, primary_key=True)
    ubigeo = db.Column(db.String(10))
    department = db.Column(db.String(255))
    
    def __init__(self, ubigeo, department):
        self.ubigeo = ubigeo
        self.department = department
    
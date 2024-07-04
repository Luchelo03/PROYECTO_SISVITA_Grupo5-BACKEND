from utils.db import db
from dataclasses import dataclass

@dataclass
class Provincia(db.Model):
    __tablename__='province'
    id: int
    ubigeo: str
    province: str
    department_id: int
    
    id = db.Column(db.Integer, primary_key=True)
    ubigeo = db.Column(db.String(10))
    province = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    
    department = db.relationship('Departamentos', backref='province')
    
    def __init__(self, ubigeo, province, department_id):
        self.ubigeo = ubigeo
        self.province = province
        self.department_id = department_id
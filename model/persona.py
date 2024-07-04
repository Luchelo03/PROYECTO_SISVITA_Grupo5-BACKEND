from utils.db import db
from dataclasses import dataclass
from model.usuario import Usuario

@dataclass
class Persona(db.Model):
    __tablename__ = 'person'
    id: int 
    first_name: str
    last_name: str
    role: str
    user_id: int 
    cell_phone: str
    department_id: int
    province_id: int
    district_id: int
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    role = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    #nuevo
    cell_phone=db.Column(db.String(9))
    department_id=db.Column(db.Integer, db.ForeignKey('department.id'))
    province_id=db.Column(db.Integer, db.ForeignKey('province.id'))
    district_id=db.Column(db.Integer, db.ForeignKey('district.id'))
    
    usuario = db.relationship('Usuario', backref='person')
    #nuevo
    department=db.relationship('Departamentos', backref='person')
    province=db.relationship('Provincia', backref='person')
    district=db.relationship('Distrito', backref='person')
    
    def __init__(self, first_name, last_name, role, user_id,cell_phone,department_id,province_id,district_id):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.user_id = user_id
        #nuevo
        self.cell_phone=cell_phone
        self.department_id=department_id
        self.province_id=province_id
        self.district_id=district_id
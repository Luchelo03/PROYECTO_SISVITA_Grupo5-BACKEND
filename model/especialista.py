from utils.db import db
from dataclasses import dataclass

@dataclass
class Especialista(db.Model):
    __tablename__='specialist'
    
    id: int
    person_id: int
    codigo_especialista: str
    specialty: str
    
    id=db.Column(db.Integer, primary_key=True)
    person_id=db.Column(db.Integer, db.ForeignKey('person.id'))
    codigo_especialista=db.Column(db.String(8), db.ForeignKey('unique_codes.code'))
    specialty=db.Column(db.String(255))
    
    person = db.relationship('Persona', backref = 'specialist')
    unique_codes = db.relationship('Codigos', backref = 'specialist')
    
    def __init__(self, person_id, codigo_especialista, specialty):
        self.person_id=person_id
        self.codigo_especialista=codigo_especialista
        self.specialty=specialty
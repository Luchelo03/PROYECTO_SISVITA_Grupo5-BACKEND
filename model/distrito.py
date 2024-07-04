from utils.db import db
from dataclasses import dataclass
from model.provincia import Provincia

@dataclass
class Distrito(db.Model):
    __tablename__ = 'district'
    id: int
    ubigeo: str
    district: str
    province_id: int
    
    id=db.Column(db.Integer, primary_key=True)
    ubigeo=db.Column(db.String(10))
    district=db.Column(db.String(255))
    province_id=db.Column(db.Integer, db.ForeignKey('province.id'))
    
    province=db.relationship('Provincia', backref='district')
    
    def __init__(self, ubigeo, district, province_id):
        self.ubigeo = ubigeo
        self.district = district
        self.province_id = province_id
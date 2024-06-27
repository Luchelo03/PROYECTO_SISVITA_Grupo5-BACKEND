from sqlalchemy import func
from utils.db import db
from dataclasses import dataclass
from model.test import Test
from model.diagnostico import Diagnostico

@dataclass
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_entidad = db.Column(db.String(8), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
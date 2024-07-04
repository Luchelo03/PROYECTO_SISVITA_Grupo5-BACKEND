from utils.ma import ma
from marshmallow import fields

class SemaforoSchema(ma.Schema):
    id = fields.Integer()
    color = fields.String()
    
semaforo_schema = SemaforoSchema()
semaforos_schema = SemaforoSchema(many=True)
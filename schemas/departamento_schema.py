from utils.ma import ma
from marshmallow import fields

class DepartamentoSchema(ma.Schema):
    id = fields.Integer()
    ubigeo = fields.String()
    department = fields.String()
    
departamento_schema = DepartamentoSchema()
departamentos_schema = DepartamentoSchema(many=True)
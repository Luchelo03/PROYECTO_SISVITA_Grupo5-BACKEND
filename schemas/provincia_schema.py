from utils.ma import ma
from model.provincia import Provincia
from schemas.departamento_schema import DepartamentoSchema
class ProvinciaSchema(ma.Schema):
    class Meta: 
        model = Provincia
        fields = ('id','ubigeo','province','department_id','department')
        
    department = ma.Nested(DepartamentoSchema)
    
provincia_schema = ProvinciaSchema()
provincias_schema = ProvinciaSchema(many=True)
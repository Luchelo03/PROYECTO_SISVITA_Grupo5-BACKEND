from utils.ma import ma
from model.distrito import Distrito
from schemas.provincia_schema import ProvinciaSchema

class DistritoSchema(ma.Schema):
    class Meta:
        model = Distrito
        fields = ('id','ubigeo','district','province_id','province')
        
    province = ma.Nested(ProvinciaSchema)
    
distrito_schema = DistritoSchema()
distritos_schema = DistritoSchema(many=True)
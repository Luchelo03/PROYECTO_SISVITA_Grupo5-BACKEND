from utils.ma import ma
from model.persona import Persona
from schemas.usuario_schema import UsuarioSchema
from schemas.departamento_schema import DepartamentoSchema
from schemas.provincia_schema import ProvinciaSchema
from schemas.distrito_schema import DistritoSchema

class PersonaSchema(ma.Schema):
    class Meta:
        model = Persona
        fields = ('id','first_name','last_name','role','user_id','cell_phone','deparment_id','province_id','district_id',
                  'usuario','department','province','district')
        
    usuario = ma.Nested(UsuarioSchema)
    department=ma.Nested(DepartamentoSchema)
    province=ma.Nested(ProvinciaSchema)
    district=ma.Nested(DistritoSchema)
    

persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True)
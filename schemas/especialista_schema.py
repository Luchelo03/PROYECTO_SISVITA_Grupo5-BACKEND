from utils.ma import ma
from model.especialista import Especialista
from schemas.persona_schema import PersonaSchema
from schemas.codigos_schema import CodigoSchema

class EspecialistaSchema(ma.Schema):
    class Meta:
        model = Especialista
        fields=('id','person_id','codigo_especialista','specialty',
                'persona','codigo')
        
    persona = ma.Nested(PersonaSchema) 
    codigo = ma.Nested(CodigoSchema)
    
especialista_schema = EspecialistaSchema()
especialistas_schema = EspecialistaSchema(many=True)
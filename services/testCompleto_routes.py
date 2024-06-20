from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.test import Test
from model.pregunta import Pregunta
from model.opcion import Opcion

test_routes = Blueprint('test_routes', __name__)

@test_routes.route('/test/new', methods=['POST'])
def create_test():
    data = request.get_json()
    
    # Crear el test
    new_test = Test(test_name=data['test_name'])
    db.session.add(new_test)
    db.session.commit()
    
    # Crear las preguntas y opciones
    for question_data in data['questions']:
        new_question = Pregunta(test_id=new_test.id, question_text=question_data['question_text'])
        db.session.add(new_question)
        db.session.commit()
        
        for option_data in question_data['options']:
            new_option = Opcion(question_id=new_question.id, option_text=option_data['option_text'], score=option_data['score'])
            db.session.add(new_option)
    
    db.session.commit()
    
    return make_response(jsonify({
        'message': 'Se creó exitosamente el Test',
        'status': 201,
        'data': {
            'test_id': new_test.id,
            'test_name': new_test.test_name
        }
    }), 201)

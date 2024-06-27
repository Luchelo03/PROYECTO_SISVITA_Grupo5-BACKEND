from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.test import Test
from model.pregunta import Pregunta
from model.opcion import Opcion
from model.diagnostico import Diagnostico
from model.resultado import Result

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

@test_routes.route('/test/submit_test', methods=['POST'])
def submit_test():
    data = request.get_json()
    user_id = data['user_id']
    test_id = data['test_id']
    answers = data['answers']

    total_score = 0
    for answer in answers:
        option = Opcion.query.filter_by(id=answer['option_id']).first()
        total_score += option.score

    diagnosis = Diagnostico.query.filter(Diagnostico.test_id == test_id, Diagnostico.min_score <= total_score, Diagnostico.max_score >= total_score).first()

    if diagnosis:
        new_result = Result(codigo_entidad=user_id, test_id=test_id, total_score=total_score, diagnosis_id=diagnosis.id)
        db.session.add(new_result)
        db.session.commit()

        return jsonify({
            'total_score': total_score,
            'diagnosis': diagnosis.diagnosis_text
        }), 200
    else:
        return jsonify({
            'message': 'Diagnosis not found for the given score'
        }), 400
        
@test_routes.route('/test/get_questions', methods=['GET'])
def get_questions():
    test_id = 1  # Asumiendo que solo hay un test o especifica el test_id necesario
    test = Test.query.filter_by(id=test_id).first()

    if not test:
        return jsonify({'message': 'Test not found'}), 404


    questions = Pregunta.query.filter_by(test_id=test.id).all()
    question_list = []

    for question in questions:
        options = Opcion.query.filter_by(question_id=question.id).all()
        option_list = [{'id': option.id, 'text': option.option_text, 'score': option.score} for option in options]
        question_list.append({'id': question.id, 'text': question.question_text, 'options': option_list})

    return jsonify({'test_name': test.test_name, 'questions': question_list})
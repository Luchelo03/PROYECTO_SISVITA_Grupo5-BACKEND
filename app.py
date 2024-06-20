from flask import Flask
from utils.db import db
from services.usuario_routes import usuario_routes
from services.persona_routes import persona_routes
from services.estudiante_routes import estudiante_routes
from services.testCompleto_routes import test_routes
from services.diagnostico_routes import diagnostico_routes
from config import DATABASE_CONNECTION
from flask import Flask
from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(usuario_routes)
app.register_blueprint(persona_routes)
app.register_blueprint(estudiante_routes)
app.register_blueprint(test_routes)
app.register_blueprint(diagnostico_routes)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
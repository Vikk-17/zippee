from flask import Flask
from models import db
from routes import api
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'test'
app.config['JWT_SECRET_KEY'] = 'jwt_test'
# app.config.from_pyfile("config.py")

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(api)

# Swagger config
swagger = Swagger(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
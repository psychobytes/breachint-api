from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

# init app & db connect
app = Flask(__name__)
CORS(app, resources={r"/admin/*": {"origins": "*"}}, supports_credentials=True)

# Konfigurasi MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl:pwl123@localhost:3306/db_flask_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
db = SQLAlchemy(app)

app.app_context().push()
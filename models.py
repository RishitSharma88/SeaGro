from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    profile_pic = db.Column(db.String(32), default = 'default.jpeg')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    rating = db.Column(db.Double, nullable=False)
    votes = db.Column(db.Integer)
    price = db.Column(db.Double, nullable=False, default=0)
    instructor = db.Column(db.String(256), nullable=False)
    course_url = db.Column(db.String(256), nullable=False)
    
with app.app_context():
    db.create_all()
from app import app
import os

app.config['NEWS_API_KEY'] = os.getenv('NEWS_API_KEY')
app.config['NEWS_API_URL'] = os.getenv('NEWS_API_URL')     
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')      
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')     
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')     
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')      

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')        
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')  
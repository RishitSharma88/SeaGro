from app import app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import url_for 
from models import User

mail = Mail(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_reset_token(user):
    return serializer.dumps(user.email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return User.query.filter_by(email=email).first()

def send_reset_email(user):
    token = generate_reset_token(user)
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''
    To reset your password, click the following link:
    {reset_url}

    If you did not make this request, simply ignore this email.
    '''
    mail.send(msg)
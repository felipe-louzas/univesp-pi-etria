from flask import current_app
from datetime import datetime, timedelta
import jwt

def generate_email_confirmation_token(email):
    payload = {
        'iss': 'etria',
        'aud': 'email',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1),
        'sub': email,
    }
    
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def check_email_validation_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'], audience='email')
        return payload['sub']
    except Exception as ex:
        print(ex)
        return None
from .models import User
from flask_login import LoginManager

from etria.models import User

login_manager = LoginManager()
login_manager.login_view = 'routes.auth.login'
login_manager.login_message = 'Sua sessão expirou. Por favor, faça login novamente.'

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

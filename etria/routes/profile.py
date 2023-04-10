from flask import Blueprint, render_template
from flask_login import login_required
from .common import email_verified

routes = Blueprint('profile', __name__)


@routes.before_request
@email_verified
def require_login():
    # Require login for all routes in this blueprint
    pass


@routes.route('/perfil')
def home():
    # Return the index.html template
    return render_template('base/empty.html')

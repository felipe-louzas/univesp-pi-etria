from flask import Blueprint, render_template
from .common import email_verified

routes = Blueprint('atendimentos', __name__)


@routes.before_request
@email_verified
def require_login():
    # Require login for all routes in this blueprint
    pass


@routes.route('/atendimentos')
def home():
    # Return the index.html template
    return render_template('base/empty.html')

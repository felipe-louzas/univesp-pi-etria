from flask import Blueprint, render_template

routes = Blueprint('public', __name__)


# Return the index.html template
@routes.route('/index.html')
def index():
    return render_template('index.html')
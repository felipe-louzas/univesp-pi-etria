from flask import Blueprint, current_app, send_from_directory, render_template

from .auth import routes as auth_routes
from .atendimentos import routes as atendimentos_routes
from .profile import routes as profile_routes
from .animais import routes as animais_routes
from .public import routes as public_routes
from .tutores import routes as tutores_routes


# Routes blueprint
#
# This is the blueprint from which all routes are registered.
# It is imported by the etria package and registered on the Flask app instance in etria/__init__.py
#
routes = Blueprint('routes', __name__)
routes.register_blueprint(public_routes)
routes.register_blueprint(auth_routes)
routes.register_blueprint(atendimentos_routes)
routes.register_blueprint(profile_routes)
routes.register_blueprint(animais_routes)
routes.register_blueprint(tutores_routes)

# 
# Register base routes
#

@routes.route('/')
def index():
    # Return the index.html template
    return render_template('index.html')


# Serve /js, /css and /img files from the app's static folder
@routes.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(current_app.static_folder + '/js', path)

@routes.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(current_app.static_folder + '/css', path)

@routes.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(current_app.static_folder + '/img', path)



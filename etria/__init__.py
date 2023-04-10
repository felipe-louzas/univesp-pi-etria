import os

from dotenv import load_dotenv
from flask import Flask

from etria.login import login_manager
from etria.assets import assets
from etria.database import database
from etria.context import inject_global_context
from etria.routes import routes
from etria.email import mail


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config.from_object(os.environ['APP_CONFIG'])
    app.register_blueprint(routes)
    app.context_processor(inject_global_context)

    assets.init_app(app)
    database.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    return app


app = create_app()

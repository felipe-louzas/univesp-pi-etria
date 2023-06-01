from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from .common import membro_equipe

from datetime import datetime

from etria import database as db
from etria.models import Tutores, User

routes = Blueprint('tutores', __name__)


@routes.before_request
@membro_equipe
def require_login():
    # Route is only accessible to membros da equipe (admin, veterinário, etc)
    pass



@routes.route('/tutores')
def home():
    tutores = Tutores.query.all()

    model = {
        'tutores': tutores
    }

    # Return the index.html template
    return render_template('tutores/index.html', model=model)


@routes.route('/tutores/<int:tutor_id>/aprovar', methods=['POST'])
def aprovar(tutor_id):
    tutor = Tutores.query.get(tutor_id)
    tutor.aprovado_em = datetime.now()
    tutor.aprovado_por = current_user.id
    db.session.commit()

    # Redirect to the index
    return redirect(url_for('routes.tutores.home'))


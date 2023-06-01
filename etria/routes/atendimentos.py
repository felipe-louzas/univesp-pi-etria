from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .common import cadastro_completo

from etria import database as db
from etria.models import Atendimentos, Tutores, MembrosEquipe, Animais

from datetime import datetime

routes = Blueprint('atendimentos', __name__)


@routes.before_request
@cadastro_completo
def require_login():
    # Require login for all routes in this blueprint
    pass


@routes.route('/atendimentos')
def home():
    if current_user.is_membro_equipe:
        atendimentos = Atendimentos.query.all()
    else:
        tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
        atendimentos = Atendimentos.query.filter_by(tutor_id=tutor.id).all()

    model = {
        'atendimentos': atendimentos
    }

    # Return the index.html template
    return render_template('atendimentos/index.html', model=model)


@routes.route('/atendimentos/novo')
def new():
    tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
    animais = Animais.query.filter_by(tutor_id=tutor.id).all()

    if tutor.aprovado_em is None:
        flash('Você precisa ter seu cadastro aprovado para realizar atendimentos.', 'warning')
        return redirect(url_for('routes.atendimentos.home'))

    model = {
        'animais': {animal.id: animal.nome for animal in animais},
        'atendimento': Atendimentos(
        ),
        'anamnese': {},
    }

    # Render template
    return render_template('atendimentos/form.html', model=model)


@routes.route('/atendimentos/<int:id>/editar')
def edit(id):
    tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
    animais = Animais.query.filter_by(tutor_id=tutor.id).all()

    atendimento = Atendimentos.query.get(id)

    model = {
        'animais': {animal.id: animal.nome for animal in animais},
        'atendimento': atendimento,
        'anamnese': eval(atendimento.anamnese),
    }

    # Render template
    return render_template('atendimentos/form.html', model=model)


@routes.route('/atendimentos/<int:id>/view')
def view(id):

    atendimento = Atendimentos.query.get(id)

    model = {
        'atendimento': atendimento,
        'anamnese': eval(atendimento.anamnese),
    }

    # Render template
    return render_template('atendimentos/view.html', model=model)


@routes.route('/atendimentos/save', methods=['POST'])
def save():
    id = request.form.get('id')

    if id is not None and id != '':
        # Get atendimento from database
        atendimento = Atendimentos.query.get(id)
        atendimento.animal_id = request.form['animal_id']
        atendimento.anamnese = str(dict(request.form))    

    else:
        tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
        
        if tutor.aprovado_em is None:
            flash('Você precisa ter seu cadastro aprovado para realizar atendimentos.', 'warning')
            return redirect(url_for('routes.atendimentos.home'))

        atendimento = Atendimentos(
            tutor_id=tutor.id,
            animal_id=request.form['animal_id'],
            atend_type='C',
            situacao='S',
            data_solicitacao=datetime.now(),
            anamnese=str(dict(request.form))
        )
        db.session.add(atendimento)

    db.session.commit()
    
    # Redirect the the list of atendimentos
    return redirect(url_for('routes.atendimentos.home'))
    
@routes.route('/atendimentos/<int:id>/cancel', methods=['POST'])
def cancel(id):
    atendimento = Atendimentos.query.get(id)
    atendimento.situacao = 'C'
    db.session.commit()
    
    # Redirect the the list of atendimentos
    return redirect(url_for('routes.atendimentos.home'))


@routes.route('/atendimentos/agendar', methods=['POST'])
def agendar():
    atendimento = Atendimentos.query.get(request.form['atendimento_id'])
    atendimento.situacao = 'A'
    atendimento.data_agendamento = datetime.strptime(request.form['data_agendamento'], '%d/%m/%Y %H:%M')
    db.session.commit()
    
    # Redirect the the list of atendimentos
    return redirect(url_for('routes.atendimentos.home'))
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user

from datetime import datetime

from .common import cadastro_completo

from etria import database as db
from etria import validation
from etria.models import Animais, Tutores


routes = Blueprint('animais', __name__)


@routes.before_request
@cadastro_completo
def require_login():
    # Require login for all routes in this blueprint
    pass


@routes.route('/animais')
def home():
    # Get animais do tutor from database
    tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
    animais = Animais.query.filter_by(tutor_id=tutor.id).all()

    # Render template
    model = {
        'tutor': tutor,
        'animais': animais
    }

    return render_template('animais/index.html', model=model)


@routes.route('/animais/cadastrar')
def new():
    # Render template
    model = {
        'animal': Animais(
            nome='',
            idade='',
            raca='',
            cor_pelagem='',
        )
    }

    return render_template('animais/form.html', model=model)


@routes.route('/animais/<int:id>/editar')
def edit(id):

    # Get animal from database
    animal = Animais.query.get(id)

    if animal is None:
        flash('Animal não encontrado', 'error')
        return redirect(url_for('animais.home'))

    if not current_user.is_membro_equipe:
        tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
        if animal.tutor_id != tutor.id:
            flash('Você não tem permissão para editar esse animal', 'error')
            return redirect(url_for('animais.home'))

    # Render template
    model = {
        'animal': animal
    }

    return render_template('animais/form.html', model=model)


@routes.route('/animais/<int:id>/delete', methods=['POST'])
def delete(id):
    # TODO: Implement delete
    pass


@routes.route('/animais/salvar', methods=['POST'])
def save():

    # Get data from form
    id = request.form.get('id')
    nome = request.form.get('nome')
    raca = request.form.get('raca')
    idade = request.form.get('idade')
    idade_type = request.form.get('idade_options')
    especie = request.form.get('especie')
    sexo = request.form.get('sexo')
    cor_pelagem = request.form.get('cor_pelagem')
    procedencia = request.form.get('procedencia')

    # Validate
    try:
        validation.required(nome, 'Nome')
        validation.required(raca, 'Raça')
        validation.required(idade, 'Idade')
        validation.required(idade_type, 'Idade')
        validation.required(especie, 'Espécie')
        validation.required(sexo, 'Sexo')
        validation.required(cor_pelagem, 'Cor da pelagem')
        validation.required(procedencia, 'Procedência')

        validation.is_positive_int(idade, 'Idade')
        validation.valid_option(idade_type, ['D', 'S', 'M', 'A'], 'Idade')
        validation.valid_option(especie, ['GATO', 'CACHORRO', 'OUTRO'], 'Espécie')
        validation.valid_option(sexo, ['M', 'F'], 'Sexo')
        validation.valid_option(procedencia, ['Criador', 'Abrigo', 'Resgate', 'Compra'], 'Procedência')

    except ValueError as err:
        flash(str(err), 'error')
        return redirect(url_for('routes.animais.new'))

    # Save to database
    tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()

    if id is None or id == '' or id == 'None':
        animal = Animais()
        animal.tutor_id = tutor.id
        db.session.add(animal)
    else:
        animal = Animais.query.get(int(id))

    if idade != animal.idade or idade_type != animal.idade_type:
        animal.idade_last_update = datetime.now()

    animal.nome = nome
    animal.raca = raca
    animal.idade = idade
    animal.idade_type = idade_type
    animal.especie = especie
    animal.sexo = sexo
    animal.cor_pelagem = cor_pelagem
    animal.procedencia = procedencia

    db.session.commit()

    # Redirect to home
    return redirect(url_for('routes.animais.home'))

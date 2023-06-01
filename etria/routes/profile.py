import os

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_login import current_user, login_user
from .common import email_verified

from datetime import datetime

from werkzeug.utils import secure_filename
from werkzeug.security import safe_join

from etria import validation
from etria import database as db
from etria.documents import make_preview, UnsupportedFileTypeError
from etria.models import MembrosEquipe, Tutores, Contatos, Cursos, User, Documentos

routes = Blueprint('profile', __name__)


@routes.before_request
@email_verified
def require_login():
    # Require login for all routes in this blueprint
    pass


@routes.route('/perfil')
def home():
    # Return the index.html template
    model = {
        'user': current_user
    }

    if current_user.is_membro_equipe:
        membro_equipe = MembrosEquipe.query.filter_by(usuario_id=current_user.id).first()
        cursos = Cursos.query.all()

        model.update({
            'membro_equipe': membro_equipe,
            'cursos': {curso.id: curso.nome for curso in cursos}
        })

    elif current_user.is_tutor:
        tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
        contato = Contatos.query.get(tutor.contato_id)

        model.update({
            'tutor': tutor,
            'contato': contato,
        })

    return render_template('perfil/index.html', model=model)


@routes.route('/documents/<int:doc_id>/preview')
def doc_preview(doc_id):
    #
    # TODO: This is a temporary solution to preview documents
    # For future generations: this is absolutely insecure and should never be used in production
    #
    doc = Documentos.query.get(doc_id)
    return doc.preview


@routes.route('/documents/<int:doc_id>/view')
def doc_view(doc_id):
    #
    # TODO: This is a temporary solution to preview documents
    # For future generations: this is absolutely insecure and should never be used in production
    #
    doc = Documentos.query.get(doc_id)

    # Return file from upload directory
    doc_dir = os.path.abspath(os.path.join(current_app.config['UPLOAD_FOLDER'], str(doc.id)))
    return send_from_directory(doc_dir, doc.filename)


#
# POST
#


@routes.route('/perfil', methods=['POST'])
def perfil_post():
    if current_user.is_membro_equipe:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        cargo = request.form.get('cargo')
        curso = request.form.get('curso')

        try:
            fname = validation.required(fname, 'Nome')
            lname = validation.required(lname, 'Sobrenome')
            cargo = validation.required(cargo, 'Cargo')
            cargo = validation.valid_option(cargo, ['ADMIN', 'VETERINARIO', 'ASSISTENTE'], 'Cargo')

            if curso is None or curso.strip() == '':
                curso = None
            else:
                validation.is_positive_int(curso, 'Curso')

        except ValueError as err:
            flash(str(err), 'danger')
            return redirect(url_for('routes.profile.home'))

        membro_equipe = MembrosEquipe.query.filter_by(usuario_id=current_user.id).first()
        membro_equipe.cargo_type = cargo
        membro_equipe.curso_id = int(curso) if curso else None

        user = User.query.get(current_user.id)
        user.first_name = fname
        user.last_name = lname
        login_user(user)

        db.session.commit()

        flash('Cadastro atualizado com sucesso!', 'success')
        return redirect(url_for('routes.profile.home'))

    elif current_user.is_tutor:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        rg = request.form.get('rg')
        cpf = request.form.get('cpf')

        cep = request.form.get('cep')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        complemento = request.form.get('complemento')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')
        telefone1 = request.form.get('telefone1')
        telefone2 = request.form.get('telefone2')

        imageDocumento = request.files.get('imageDocumento')
        imageCompEnd = request.files.get('imageCompEnd')
        imageCompRenda = request.files.get('imageCompRenda')

        try:
            validation.required(fname, 'Nome')
            validation.required(lname, 'Sobrenome')
            validation.required(rg, 'RG')
            validation.required(cpf, 'CPF')
            validation.required(cep, 'CEP')
            validation.required(logradouro, 'Logradouro')
            validation.required(numero, 'Número')
            validation.required(bairro, 'Bairro')
            validation.required(cidade, 'Cidade')
            validation.required(uf, 'UF')

            cpf = validation.cpf(cpf, 'CPF')
            rg = validation.rg(rg, 'RG')
            cep = validation.numeric(cep, 'CEP', length=8)
            uf = validation.valid_option(uf, ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                                              'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                                              'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'], 'UF')

            if complemento is None or complemento.strip() == '':
                complemento = None

            if telefone1 is None or telefone1.strip() == '':
                telefone1 = None
            else:
                telefone1 = validation.numeric(telefone1, 'Telefone 1', min_length=10, max_length=11)

            if telefone2 is None or telefone2.strip() == '':
                telefone2 = None
            else:
                telefone2 = validation.numeric(telefone2, 'Telefone 2', min_length=10, max_length=11)

        except ValueError as err:
            flash(str(err), 'danger')
            return redirect(url_for('routes.profile.home'))

        tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
        contato = Contatos.query.get(tutor.contato_id)

        # If no documents have been uploaded, check that the tutor already has documents
        if not imageDocumento or not imageCompEnd or not imageCompRenda:
            if not tutor.identidade_doc_id or not tutor.comp_endereco_doc_id or not tutor.comp_renda_doc_id:
                flash('É necessário enviar os documentos para concluir o cadastro!', 'danger')
                return redirect(url_for('routes.profile.home'))

        # Update database

        # Update user
        user = User.query.get(current_user.id)
        user.first_name = fname
        user.last_name = lname
        login_user(user)

        # Update tutor
        tutor.rg = rg
        tutor.cpf = cpf

        # Update contato
        contato.nome = fname + ' ' + lname
        contato.nome_resp = fname + ' ' + lname
        contato.cep = cep
        contato.logradouro = logradouro
        contato.numero = numero
        contato.complemento = complemento
        contato.bairro = bairro
        contato.cidade = cidade
        contato.uf = uf
        contato.telefone1 = telefone1
        contato.telefone2 = telefone2

        cadastro_updated = False

        # If user, tutor or contato has been updated, update the atualizado_em field and set aprovado_em e aprovado_por to null
        if db.session.is_modified(user) or db.session.is_modified(tutor) or db.session.is_modified(contato):
            cadastro_updated = True

        # Insert or update documents
        if imageDocumento and imageDocumento.filename != '':
            cadastro_updated = True
            tutor.identidade_doc_id = _update_documento(tutor.identidade_doc_id, imageDocumento)

        if imageCompEnd and imageCompEnd.filename != '':
            cadastro_updated = True
            tutor.comp_endereco_doc_id = _update_documento(tutor.comp_endereco_doc_id, imageCompEnd)

        if imageCompRenda and imageCompRenda.filename != '':
            cadastro_updated = True
            tutor.comp_renda_doc_id = _update_documento(tutor.comp_renda_doc_id, imageCompRenda)

        if cadastro_updated:
            tutor.atualizado_em = datetime.now()
            tutor.aprovado_em = None
            tutor.aprovado_por = None

        db.session.commit()

        flash('Cadastro atualizado com sucesso!', 'success')
        return redirect(url_for('routes.profile.home'))


def _update_documento(doc_id, image):
    filename = secure_filename(image.filename)
    doc_bytes = image.read()
    preview = make_preview(image.mimetype, doc_bytes)

    if doc_id:
        doc = Documentos.query.get(doc_id)
        doc.filename = filename
        doc.uploaded_at = datetime.now()
        doc.filesize = len(doc_bytes)
        doc.preview = preview
    else:
        doc = Documentos(
            filename=filename,
            uploaded_at=datetime.now(),
            filesize=len(doc_bytes),
            preview=preview
        )
        db.session.add(doc)
        db.session.flush()

    _save_file(doc.id, filename, doc_bytes)
    return doc.id


def _save_file(doc_id, filename, doc_bytes):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], str(doc_id))
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath = os.path.join(filepath, filename)
    with open(filepath, 'wb') as f:
        f.write(doc_bytes)

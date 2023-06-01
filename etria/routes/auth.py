from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from etria.models import User, Tutores, Contatos
from etria.database import database as db
from etria.email import send_verification_email
from etria.jwt import check_email_validation_token

from .common import logout_required

routes = Blueprint('auth', __name__)


#
# GET
#


@routes.route('/login')
@logout_required
def login():
    next_page = request.args.get('next') or ''
    return render_template('auth/login.html', next_page=next_page)


@routes.route('/cadastro')
@logout_required
def cadastro():
    return render_template('auth/cadastro.html')


@routes.route('/recover')
@logout_required
def recover():
    return render_template('auth/recover.html')


@routes.route('/verify')
@login_required
def verify():
    if current_user.email_verified:
        return redirect(url_for('routes.atendimentos.home'))
    return render_template('auth/verify.html', email=current_user.email)


@routes.route('/update-email')
@login_required
def update_email():
    # Get the referer route or default to routes.auth.login
    cancel_url = request.referrer or url_for('routes.auth.login')
    return render_template('auth/update_email.html', email=current_user.email, cancel_url=cancel_url)


@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


@routes.route('/confirm-email/<token>')
def confirm_email(token):
    email = check_email_validation_token(token)

    user = None
    if email:
        user = User.query.filter_by(email=email).first()

    if not user:
        flash('O link de confirmação é inválido ou expirou.', 'danger')

        if current_user.is_authenticated:
            return redirect(url_for('routes.auth.verify'))
        else:
            return redirect(url_for('routes.auth.login'))

    user.email_verified = True
    db.session.commit()

    if not current_user.is_authenticated:
        login_user(user)

    return redirect(url_for('routes.atendimentos.home'))


#
# POST
#


@routes.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    login = request.form.get('login')
    password = request.form.get('password')

    user = User.query.filter_by(email=login).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Usuário ou senha incorretos. Verifique e tente novamente.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('routes.auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user)

    next_page = request.form.get('nextPage')
    return redirect(next_page or url_for('routes.atendimentos.home'))


@routes.route('/cadastro', methods=['POST'])
def cadastro_post():
    # code to validate and add user to database goes here
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    verify_password = request.form.get('verifyPassword')

    if password != verify_password:
        flash('As senhas informadas não conferem. Verifique e tente novamente.', 'danger')
        return redirect(url_for('routes.auth.cadastro'))

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email já cadastrado. Verifique os dados informados e tente novamente.', 'danger')
        return redirect(url_for('routes.auth.cadastro'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password, method='sha256'),
        email_verified=False,
    )
    db.session.add(new_user)

    tutor_contato = Contatos(
        nome=first_name + ' ' + last_name,
        nome_resp=first_name + ' ' + last_name,
        email=email,
    )
    db.session.add(tutor_contato)
    db.session.flush()

    tutor_cadastro = Tutores(
        usuario_id=new_user.id,
        contato_id=tutor_contato.id,
    )
    db.session.add(tutor_cadastro)

    db.session.commit()

    login_user(new_user)
    send_verification_email(current_user.email)

    return redirect(url_for('routes.auth.login'))


@routes.route('/verify', methods=['POST'])
@login_required
def verify_post():
    send_verification_email(current_user.email)
    flash('O e-mail de confirmação foi reenviado.', 'success')
    return redirect(url_for('routes.auth.verify'))


@routes.route('/recover', methods=['POST'])
def recover_post():
    # TODO: Implement recover password
    flash('Ainda não implementado.', 'danger')
    return redirect(url_for('routes.auth.recover'))


@routes.route('/update-email', methods=['POST'])
@login_required
def update_email_post():
    # TODO: Implement update e-mail
    flash('Ainda não implementado.', 'danger')
    return redirect(url_for('routes.auth.update_email'))

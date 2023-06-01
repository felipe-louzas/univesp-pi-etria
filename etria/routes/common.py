from functools import wraps
from flask import redirect, url_for, flash
from flask_login import login_required, current_user

from etria.models import Tutores


def logout_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('routes.atendimentos.home'))

        return func(*args, **kwargs)
    return decorated_view


def email_verified(func):

    @login_required
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.email_verified:
            return redirect(url_for('routes.auth.verify'))

        return func(*args, **kwargs)

    return decorated_view


#
# All the extra decorators below are used to restrict access to certain pages and depend on the email_verified decorator
# 

def membro_equipe(func):

    @email_verified
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_membro_equipe:
            return redirect(url_for('routes.atendimentos.home'))
        
        return func(*args, **kwargs)

    return decorated_view


def cadastro_completo(func):

    @email_verified
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.cadastro_completo:
            if current_user.is_membro_equipe:
                current_user.cadastro_completo = True
            
            elif current_user.is_tutor:
                tutor = Tutores.query.filter_by(usuario_id=current_user.id).first()
                if tutor.atualizado_em:
                    current_user.cadastro_completo = True
                else:
                    flash('Você precisa concluir seu cadastro antes de continuar.', 'info')
                    return redirect(url_for('routes.profile.home'))

        return func(*args, **kwargs)

    return decorated_view

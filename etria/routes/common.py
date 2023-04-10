from functools import wraps
from flask import redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user


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

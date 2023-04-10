from flask import current_app, render_template, url_for
from flask_mail import Mail, Message

from etria.context import site_context
from etria.jwt import generate_email_confirmation_token


mail = Mail()


def send_verification_email(email_to):
    token = generate_email_confirmation_token(email_to)
    confirm_url = url_for("routes.auth.confirm_email", token=token, _external=True)
    template = render_template(
        'auth/verification_email.html',
        confirm_url=confirm_url
    )

    msg = Message(
        f'Confirme seu email - {site_context.site_title}',
        recipients=[email_to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
    )
    mail.send(msg)

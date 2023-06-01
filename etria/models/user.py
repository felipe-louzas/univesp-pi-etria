from flask_login import UserMixin
from etria.database import database as db

class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    email_verified = db.Column(db.Boolean())
    password = db.Column(db.String(64))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    tipo_cadastro = db.Column(db.String(1)) # E = Membro Equipe, T = Tutor

    @property
    def is_membro_equipe(self):
        return self.tipo_cadastro == 'E'
    
    @property
    def is_tutor(self):
        return self.tipo_cadastro == 'T'

    @property
    def cadastro_completo(self):
        if not hasattr(self, '_cadastro_completo'):
            return False
        return getattr(self, '_cadastro_completo')
    
    @cadastro_completo.setter
    def cadastro_completo(self, value):
        setattr(self, '_cadastro_completo', value)
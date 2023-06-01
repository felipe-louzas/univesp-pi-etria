from etria.database import database as db


class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))


class MembrosEquipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    cargo_type = db.Column(db.String(32))  # ADMIN, VETERINARIO, ASSISTENTE


class Tutores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rg = db.Column(db.String(15))
    cpf = db.Column(db.String(11))
    identidade_doc_id = db.Column(db.Integer, db.ForeignKey('documentos.id'))
    comp_endereco_doc_id = db.Column(db.Integer, db.ForeignKey('documentos.id'))
    comp_renda_doc_id = db.Column(db.Integer, db.ForeignKey('documentos.id'))
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), nullable=False)
    atualizado_em = db.Column(db.DateTime)
    aprovado_em = db.Column(db.DateTime)
    aprovado_por = db.Column(db.Integer, db.ForeignKey('membros_equipe.id'))

    usuario = db.relationship('User')
    contato = db.relationship('Contatos')


class Animais(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutores.id'))
    nome = db.Column(db.String(255))
    especie = db.Column(db.String(255))
    raca = db.Column(db.String(255))
    idade = db.Column(db.Integer)
    idade_type = db.Column(db.String(1))
    idade_last_update = db.Column(db.DateTime)
    sexo = db.Column(db.String(1))
    cor_pelagem = db.Column(db.String(255))
    procedencia = db.Column(db.String(255))


class Vacinas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    vacina_type = db.Column(db.String(255))


class Documentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime)
    removed_at = db.Column(db.DateTime)
    filesize = db.Column(db.Integer)
    preview = db.Column(db.LargeBinary)

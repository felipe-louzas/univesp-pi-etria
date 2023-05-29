from etria.database import database as db


class Especialidades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    abre_agendamento = db.Column(db.Boolean())


class Encaminhamentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    agendamento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'))
    observacoes = db.Column(db.String(255))


class EspecialidadesIndicacoes(db.Model):
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), primary_key=True)
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), primary_key=True)


class Contatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    nome_resp = db.Column(db.String(255))
    telefone1 = db.Column(db.String(16))
    telefone2 = db.Column(db.String(16))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(255))
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    uf = db.Column(db.String(2))
    cep = db.Column(db.String(8))
    email = db.Column(db.String(255))
    site = db.Column(db.String(255))
    observacoes = db.Column(db.String(255))

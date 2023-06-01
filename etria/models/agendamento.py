from etria.database import database as db


class Atendimentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutores.id'))
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    atend_type = db.Column(db.String(1))  # C = Consulta, R = Retorno
    situacao = db.Column(db.String(1))  # S = Solicitado A = Agendado, R = Realizado, C = Cancelado
    data_solicitacao = db.Column(db.DateTime)
    data_agendamento = db.Column(db.DateTime)
    discente_id = db.Column(db.Integer, db.ForeignKey('membros_equipe.id'))
    vet_resp_id = db.Column(db.Integer, db.ForeignKey('membros_equipe.id'))
    retorno_ind = db.Column(db.Integer)  # 0 = Em caso de piora ou recidiva, ou numero de semanas
    retorno_atend_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'))
    anamnese = db.Column(db.Text)

    animal = db.relationship('Animais')
    tutor = db.relationship('Tutores')


class Anamneses(db.Model):
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'), primary_key=True)
    peso = db.Column(db.Integer())


class SintomasCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))


class Sintomas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('sintomas_category.id'))
    name = db.Column(db.String(255))
    descricao = db.Column(db.String(255))


class AnamneseSintomas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'))
    sintoma_id = db.Column(db.Integer, db.ForeignKey('sintomas.id'))
    frequencia_type = db.Column(db.String(1))  # D = dias, S = semanas, M = meses, A = anos
    duracao = db.Column(db.Integer)
    duracao_type = db.Column(db.String(1))  # D = dias, S = semanas, M = meses, A = anos
    similar_contato_type = db.Column(db.String(1))
    observacoes = db.Column(db.String(255))


class AnamneseTratamentos(db.Model):
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'), primary_key=True)
    tratamento_id = db.Column(db.Integer, db.ForeignKey('eventos_tratamentos.id'), primary_key=True)

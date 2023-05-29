from etria.database import database as db


class EventosVacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    vacina_id = db.Column(db.Integer, db.ForeignKey('vacinas.id'))
    data_aplicacao = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)


class EventosReproducao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    event_type = db.Column(db.String(1))
    data_evento = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)


class EventosConvivio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    sibling_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    especie_type = db.Column(db.String(1))
    descricao = db.Column(db.String(255))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)


class EventosDiagnosticos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    data_diagnostico = db.Column(db.Date)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnosticos.id'))
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)


class EventosTratamentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('eventos_diagnosticos.id'))
    tratamento_id = db.Column(db.Integer, db.ForeignKey('prescricoes.id'))
    data_tratamento = db.Column(db.Date)
    dosagem = db.Column(db.Integer)
    dosagem_type = db.Column(db.String(1))
    duracao = db.Column(db.Integer)
    duracao_type = db.Column(db.String(1))
    resposta_type = db.Column(db.String(1))
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)


class HistoricoAlimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    data_historico = db.Column(db.Date)
    last_update = db.Column(db.Boolean())
    alimentaco_type = db.Column(db.String(1))
    marca = db.Column(db.String(255))
    frequecia = db.Column(db.Integer)
    orientacao_vet = db.Column(db.Boolean())
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)


class HistoricoDomicilio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'))
    data_historico = db.Column(db.Date)
    last_update = db.Column(db.Boolean())
    domicilio_cat = db.Column(db.String(32))
    domicilio_type = db.Column(db.String(32))
    observacoes = db.Column(db.Text)
    cadastrado_em = db.Column(db.DateTime)
    removido_em = db.Column(db.DateTime)

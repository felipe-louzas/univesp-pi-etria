import enum
from etria.database import database as db


class Exames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exame_type = db.Column(db.String(1))
    nome = db.Column(db.String(255))
    descricao = db.Column(db.Text())
    incluir_auto = db.Column(db.Boolean())


class TipoResultado(enum.Enum):
    MEASUREMENT = 'Medição'
    LIST = 'Lista'
    BOOL = 'Indicador'
    TEXT = 'Texto'


class ExamesObservacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exame_id = db.Column(db.Integer, db.ForeignKey('exames.id'))
    nome = db.Column(db.String(255))
    descricao = db.Column(db.Text())
    resultado_type = db.Column(db.Enum(TipoResultado))
    resultado_scale = db.Column(db.String(5))
    ref_min = db.Column(db.Integer)
    ref_max = db.Column(db.Integer)
    ref_ind = db.Column(db.Boolean())
    incluir_auto = db.Column(db.Boolean())


class ObservacoesOpcoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obs_id = db.Column(db.Integer, db.ForeignKey('exames_observacoes.id'))
    resultado = db.Column(db.String(255))
    ind_ref = db.Column(db.Boolean())
    descricao_template = db.Column(db.Text)


class ExamesResultados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'))
    exame_id = db.Column(db.Integer, db.ForeignKey('exames.id'))
    resp_id = db.Column(db.Integer, db.ForeignKey('membros_equipe.id'))
    descricao = db.Column(db.String(255))


class ObservacoesResultados(db.Model):
    resultado_id = db.Column(db.Integer, db.ForeignKey('exames_resultados.id'), primary_key=True)
    obs_id = db.Column(db.Integer, db.ForeignKey('exames_observacoes.id'), primary_key=True)
    resultado = db.Column(db.String(255))
    descricao = db.Column(db.Text)

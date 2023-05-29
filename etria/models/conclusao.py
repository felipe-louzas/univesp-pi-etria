import enum
from etria.database import database as db


class Diagnosticos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    descricao = db.Column(db.Text())


class TipoPrescricao(enum.Enum):
    EXAME = "Exame"
    MEDICAMENTO = "Medicamento"
    CIRURGIA = "Cirurgia"
    GERAL = "Geral"


class Prescricoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescricao_type = db.Column(db.Enum(TipoPrescricao))
    name = db.Column(db.String(255))
    encaminhamento = db.Column(db.Boolean())
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    template = db.Column(db.Text())
    active = db.Column(db.Boolean())


class TipoDiagnostico(enum.Enum):
    SUSPEITA_CLINICA = "Suspeita clínica"
    DIAGNOSTICO_DIFERENCIAL = "Diagnóstico diferencial"


class PrescricoesPadrao(db.Model):
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnosticos.id'), primary_key=True)
    prescricao_id = db.Column(db.Integer, db.ForeignKey('prescricoes.id'), primary_key=True)
    diagnostico_type = db.Column(db.Enum(TipoDiagnostico))


class ConclusaoDiagnosticos(db.Model):
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'), primary_key=True)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnosticos.id'), primary_key=True)
    diagnostico_type = db.Column(db.Enum(TipoDiagnostico))
    observacoes = db.Column(db.Text)


class ConclusaoPrescricoes(db.Model):
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimentos.id'), primary_key=True)
    prescricao_id = db.Column(db.Integer, db.ForeignKey('prescricoes.id'), primary_key=True)
    dosagem = db.Column(db.Integer)
    dosagem_type = db.Column(db.String(32))
    duracao = db.Column(db.Integer)
    duracao_type = db.Column(db.String(32))
    encaminhamento_id = db.Column(db.Integer, db.ForeignKey('encaminhamentos.id'))
    observacoes = db.Column(db.Text)

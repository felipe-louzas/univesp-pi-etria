import os
import datetime

import etria.models

from werkzeug.security import generate_password_hash

from etria import create_app
from etria.database import database

if __name__ == '__main__':
    try:
        os.remove('instance/db.sqlite')
    except FileNotFoundError:
        pass

    app = create_app()
    with app.app_context():
        database.create_all()

        # Create curso de vetinária
        curso = etria.models.Cursos(
            nome = 'Medicina Veterinária',
        )
        database.session.add(curso)

        #
        # Create the admin user
        #

        admin = etria.models.User(
            email = 'admin@etria.com.br',
            email_verified = True,
            password = generate_password_hash('admin', method='sha256'),
            first_name = 'Administrador',
            last_name = 'ETRIA',
            tipo_cadastro = 'E'
        )
        database.session.add(admin)
        database.session.flush()

        admin_cadastro = etria.models.MembrosEquipe(
            usuario_id = admin.id,
            cargo_type = 'ADMIN'
        )
        database.session.add(admin_cadastro)

        #
        # Create veterinário user
        #

        vet = etria.models.User(
            email = 'vet@etria.com.br',
            email_verified = True,
            password = generate_password_hash('vet', method='sha256'),
            first_name = 'Veterinário',
            last_name = 'Demo',
            tipo_cadastro = 'E'
        )
        database.session.add(vet)
        database.session.flush()

        vet_cadastro = etria.models.MembrosEquipe(
            usuario_id = vet.id,
            cargo_type = 'VETERINARIO'
        )
        database.session.add(vet_cadastro)

        #
        # Create the tutor user
        #

        tutor = etria.models.User(
            email = 'tutor@etria.com.br',
            email_verified = True,
            password = generate_password_hash('tutor', method='sha256'),
            first_name = 'Tutor',
            last_name = 'Demo',
            tipo_cadastro = 'T'
        )
        database.session.add(tutor)

        tutor_contato = etria.models.Contatos(
            nome = 'Tutor Demo',
            nome_resp = 'Tutor Demo',
            telefone1 = '1112345678',
            telefone2 = '11123456789',
            logradouro = 'Rua Demo',
            numero = '123',
            complemento = 'Apt 03',
            bairro = 'Centro',
            cidade = 'São Paulo',
            uf = 'SP',
            cep = '12345678',
            email = 'tutor@etria.com.br',
            site = '',
            observacoes = ''
        )
        database.session.add(tutor_contato)
        database.session.flush()

        tutor_cadastro = etria.models.Tutores(
            usuario_id = tutor.id,
            rg = '123456789',
            cpf = '12345678901',
            contato_id = tutor_contato.id,
            atualizado_em = datetime.datetime.now()
        )
        database.session.add(tutor_cadastro)

        database.session.commit()

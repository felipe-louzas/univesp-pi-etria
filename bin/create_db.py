import os

import etria.models

from werkzeug.security import generate_password_hash

from etria import create_app
from etria.database import database

if __name__ == '__main__':
    os.remove('instance/db.sqlite')

    app = create_app()
    with app.app_context():
        database.create_all()

        # Create the admin user
        admin = etria.models.User(
            email = 'admin@etria.com.br',
            email_verified = True,
            password = generate_password_hash('admin', method='sha256'),
            first_name = 'ETRIA',
            last_name = 'Admin'
        )
        database.session.add(admin)
        database.session.commit()

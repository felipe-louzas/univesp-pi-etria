import os
from flask_assets import Environment

# Diretório base da aplicação
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


assets = Environment()
assets.from_yaml(f'{BASE_DIR}/static/assets/bundles.yaml')

from pathlib import Path

import os

API_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__))) / '..'
BROWSER_URL = os.environ.get('BROWSER_URL', 'http://localhost:3000')
ENV = os.environ.get('ENV', 'development')
IS_DEV = ENV == 'development'
IS_PROD = ENV == 'production'
LOG_LEVEL_INFO = 20
LOG_LEVEL = int(os.environ.get('LOG_LEVEL', LOG_LEVEL_INFO))

API_URL = 'localhost' if IS_DEV else 'https://api.makemegreen.fr'

STORAGE_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / '..' / 'static'

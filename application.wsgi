env_path = '/home/quest/code/flask_explog/venv/bin/

import sys
sys.path.insert(0, '/home/quest/code/flask_explog')
from apps.app import create_app
application = create_app()

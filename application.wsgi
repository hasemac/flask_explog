proj_path = '/home/quest/code/flask_explog'

import sys
sys.path.insert(0, proj_path)

import os
from dotenv import load_dotenv
load_dotenv(os.path.join(proj_path, '.env'))

from apps.app import create_app
application = create_app('local')

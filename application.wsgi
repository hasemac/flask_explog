#activator = '/home/quest/code/flask_explog/venv/bin/activate_this.py'  
#with open(activator) as f:
#    exec(f.read(), {'__file__': activator})

import sys
sys.path.insert(0, '/home/quest/code/flask_explog')
from apps.app import create_app
application = create_app('local')

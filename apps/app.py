import logging
import signal
import sys
from pathlib import Path

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

#def handler(signal, frame):
#    print('CTRL-C pressed!')
#    sys.exit(0)
#signal.signal(signal.SIGINT, handler)
#signal.pause()

# SQLAlchemyのインスタンス化
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_key):
    # Flaskインスタンス生成
    app = Flask(__name__)
    app.config.from_object(config[config_key])
    
    app.logger.setLevel(logging.DEBUG)
    
    # SQLAlchemyとアプリを連携
    db.init_app(app)
    # CSRFとアプリを連携
    csrf.init_app(app)
    # Migrateとアプリを連携
    Migrate(app, db)
    
    toolbar = DebugToolbarExtension(app)
    
    
    from apps.explog import views as explog_views
    
    app.register_blueprint(explog_views.explog, url_prefix="/explog")
    return app
    
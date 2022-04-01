import os
from pathlib import Path

basedir = Path(__file__).parent.parent


# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.getenv('FLASK_WTF_CSRF_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # これがないと警告が出るらしい
    
    
    
# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL_PROD')

# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL_TEST')
    DEBUG_TB_INTERCEPT_REDIRECTS = False # デバッグバーを表示させるときはFalse
    SQLALCHEMY_ECHO = True # SQL文がコンソールに出力される。
    
# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}

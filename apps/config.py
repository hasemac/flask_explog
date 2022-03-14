from pathlib import Path

basedir = Path(__file__).parent.parent


# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"
    SQLALCHEMY_DATABASE_URI = "mysql://aiadmin:zeDm3HLcBx@192.168.0.122/explog"
    
# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}

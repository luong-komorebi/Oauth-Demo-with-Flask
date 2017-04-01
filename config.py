class Config(object):
    """
    Common Config
    """

class DevelopmentConfig(Config):
    """
    Development Config
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production Config
    """
    DEBUG = False

app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}


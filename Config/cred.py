class DevConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    FLASKENV = 'development'
    MQ_URL = 'amqp://pika:start1234@54.65.98.165:5672'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@18.212.243.182/my-sql'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://amit:amit@192.168.1.9/Starter_APP'
    POSTGRES_SECRET_KEY = 'KOKE92jdwdm(@#Jdkmkcm93)eeijdijioHOUIHDUENJNEOINDIWIONDKWOIDNIOENDIOJIODNNCUIBYRGYVBRVTRBNOXE'
    CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@54.65.98.165:5672'
    CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@54.65.98.165:5672'
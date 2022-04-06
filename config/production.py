from config.default import *
from logging.config import dictConfig

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user='dbmasteruser',
    pw='V^UD6}wh2Esb5{?$o?IFm3&iv=&U!8h*',
    url='ls-b41f3b1d4f7b565b81eb6467fffc2a04219701a0.cusegwfp7qso.ap-northeast-2.rds.amazonaws.com',
    db='flask_pybo'
)
'''
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x90\xd5{\xa8\xfe0v\x8dO\x8dO,Hc\xddb'
'''

dictConfig({
    'version' : 1,
    'formatters' : {
        'default' : {
            'format' : '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler', # 로그 핸들러 클래스, RotatingFileHandler를 사용.
            'filename': os.path.join(BASE_DIR, 'logs/myproject.log'),   # 로그 파일명
            'maxBytes': 1024 * 1024 * 5, # 5 MB
            'backupCount' : 5,  # 로그 파일의 개수, 로그 파일을 총 5개 유지하도록 설정
            'formatter' : 'default',    # 포맷터, default 설정
        },
    },
    'root' : {  # 최상위 로거
        'level' : 'INFO',
        'handlers' : ['file']
    }
})
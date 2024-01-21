from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db/data.sqlite3')
Base = declarative_base()

def init_db():
    from .models import Distribution
    from .models import ApiLastRequest
    # データベースの初期化
    Base.metadata.create_all(bind=engine)
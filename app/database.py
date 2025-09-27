#db connection page
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin123@0.0.0.0:5432/fastapi'  #username , password , ip addr,hostname ,dbname

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base=declarative_base()

# dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
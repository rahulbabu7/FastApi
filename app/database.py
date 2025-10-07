from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from psycopg2.extras import RealDictCursor
# import psycopg2
from .config import settings
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'  #username , password , ip addr,hostname ,dbname

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
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='0.0.0.0',  # This should work if the app and postgres are on the same network
#             database='fastapi',
#             user='admin',
#             password='admin123',
#             cursor_factory=RealDictCursor
# # Returns rows as tuples.

# psycopg2.extras.RealDictCursor: Returns rows as dictionaries.

# psycopg2.extras.NamedTupleCursor: Returns rows as named tuples, so you can access columns like attributes (row.id, row.name, etc.).
#         )

#         cursor = conn.cursor()
#         print("Db up")
#         break
#     except Exception as error:
#         print("Db not connected")
#         print("error",error)
#         time.sleep(3)

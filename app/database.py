from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# -------------------- these are for db connection
from psycopg2.extras import RealDictCursor
import psycopg2 
import time


from .config import settings

# this should be somewhere else
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/webAPIpy'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# while True:
#     try:
#         # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#         # cursor = cnxn.cursor()        
#         # Connect to your postgres DB
#         conn = psycopg2.connect(host='localhost', database='webAPIpy', user='postgres', 
#             password='password123', cursor_factory=RealDictCursor)
#         # Open a cursor to perform database operations
#         cur = conn.cursor()
#         print("Database connection was succesfull!")   
#         break
#     except Exception as error:
#             print("connection to database failded")
#             print("Error:", error)
#             time.sleep(2)

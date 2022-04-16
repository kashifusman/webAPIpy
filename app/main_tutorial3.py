from ast import Try, While
from enum import auto
from importlib.resources import contents
from logging import exception
import time
from turtle import title
from typing import Optional,List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2 
# to fetching the column names and converting into dict object
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import post,user, auth


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        # cursor = cnxn.cursor()        
        # Connect to your postgres DB
        conn = psycopg2.connect(host='localhost', database='webAPIpy', user='postgres', 
            password='password123', cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("Database connection was succesfull!")   
        break
    except Exception as error:
            print("connection to database failded")
            print("Error:", error)
            time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}




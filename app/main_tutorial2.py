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
from . import models,schemas,utils
from .database import engine, get_db



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

@app.get("/")
def root():
    return {"message": "Welcome to my API"}


#Get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    ## ===================================== using Alchemy ORM =================================
    posts = db.query(models.Post).all()
    return  posts



# Get Post by Id
@app.get("/post/{id}", response_model=schemas.Post)
def get_post(id: int,response: Response, db: Session = Depends(get_db)):
    post =  db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"post with id : {id} not found")

    return  post




#Create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.dict())

    db.add(new_post)
    # it will make changes
    db.commit()
    #its like returning type 
    db.refresh(new_post)

    # need to convert this new_post to pyndetic model, because its a SQLalchemy model 
    # to convert it to pyndentic add config in schema post class
    return  new_post


#Delete post by id
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist!")
    
    post.delete(synchronize_session=False)
    db.commit()
    #if id doesnt exist then it will error 500 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update post by id
@app.put("/post/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist!")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED,  response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #Create hash passowd : hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    db.add(new_user)
    # it will make changes
    db.commit()
    #its like returning type 
    db.refresh(new_user)

    # need to convert this new_post to pyndetic model, because its a SQLalchemy model 
    # to convert it to pyndentic add config in schema post class
    return  new_user


@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exists")

    return user

from ast import Try, While
from importlib.resources import contents
from logging import exception
import time
from turtle import title
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2 
# to fetching the column names and converting into dict object
from psycopg2.extras import RealDictCursor
# import pyodbc  {for SQLServer Database}
# import itertools
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine, get_db
# server = 'CRKRL-USMANKAS2' 
# database = 'fastAPI' 
# username = 'sa' 
# password = 'sa'


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
        # cursor.execute("SELECT @@version;") 
        # row = cursor.fetchone() 
        # while row: 
        #     print(row[0])
        #     row = cursor.fetchone()

 #optional filed
    # rating: Optional[int] = None # full optional filed if user doest provide it would be none
    # my_posts = [
    #     {"id":1, "title": "title of post1", "content" : "content of post 1"},
    #     {"id":2, "title": "title of post2", "content" : "content of post 2"},
    #     {"id":3, "title": "title of post3", "content" : "content of post 3"},
    #     ]

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

    # Test method Alchemy
    # @app.get("/sqlalchemy")
    # def test_posts(db: Session = Depends(get_db)):
    #     posts = db.query(models.Post).all()
    #     return {"data": posts}

    # def find_post(id):
    #     for p in my_posts:
    #         if p["id"] == id:
    #             return p

    # def find_index_post(id):
    #     for i,p in enumerate(my_posts):
    #         if p['id'] == id:
    #             return i


@app.get("/post/{id}")
def get_post(id: int,response: Response, db: Session = Depends(get_db)):
    #print(id)
    #post = find_post(int(id)) its define in parameter so no need to convert
    # post = find_post(id)
    # cur.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    # post = cur.fetchone()
    post =  db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"post with id : {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND -- Replace all this with above code
        #return {'message': f"post with id : {id} not found"}
    return {"post_Details": post}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    ## cur.execute("""SELECT id,title,contents,published FROM posts""")
    # column_names =  cursor.columns(table='posts')
    ## records = cur.fetchall()
    # insertObject = []
    # columnNames = [column[0] for column in cursor.description]
    # for record in records:
    #     insertObject.append(dict(zip(columnNames, record)))
    #data = [dict(itertools.izip(column_names, row)) for row in cursor.fetchall()]    
    # data = cursor.execute("""SELECT id,title,content,published FROM posts""")
    # for row in cursor.columns(table='posts'):
    #     print(row.column_name)
    # for column in data.description:
    #     print(column[0])    
    # posts = cursor.fetchall()
    # print(posts)
    # print(my_posts)
    # for row in data:
    #     print(row)    
    # print(posts)
    ## ===================================== using Alchemy ORM =================================
    posts = db.query(models.Post).all()
    return {"data": posts}

    #@app.po("/createposts")
    #def create_posts(payLoad: dict = Body(...)):
    #print(payLoad)
    #    return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # ----------------------------------- direct SQL method
    # print(post)
    # try:
    #     cur.execute("""INSERT INTO posts (title,contents,published) VALUES (%s,%s,%s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    #     new_post = cur.fetchone()
    #     conn.commit()
    # except Exception as error:
    #     print(error)
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # print(post)
    # print(post.dict()) # this will convert payload into pydentic model

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # if you have many field then the easy way to do it is
    #print(**post.dict()) # unpack post dict object to convert 
    new_post = models.Post(**post.dict())


    db.add(new_post)
    # it will make changes
    db.commit()
    #its like returning type 
    db.refresh(new_post)

    return {"new_post": new_post}

# title str, content str {validation} 


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    # print(id)
    # cur.execute(""" DELETE FROM posts where id = %s RETURNING *""", (str(id)))
    # deletedPost = cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    #index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist!")
    
    post.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    #return {'message': "post was successfully deleted"}
    #if id doesnt exist then it will error 500 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_posts(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # print(id)
    # index = find_index_post(id)
    # cur.execute(""" UPDATE posts SET title=%s, contents=%s, published=%s WHERE id = %s returning * """,
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with {id} does not exist!")
    # print(index)
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # return {'message': "post was successfully deleted"}
    # if id doesnt exist then it will error 500 
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    #index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist!")
    
    # post_query.update({'title':'this is updated title', 'content': 'this is updated content'}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
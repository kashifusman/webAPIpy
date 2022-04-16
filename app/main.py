from fastapi import FastAPI
# to fetching the column names and converting into dict object
from . import models
from .database import engine
from .routers import post,user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# Once alembic implimented no longer required this , this is for model to table creation manully
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#change origins to array

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}




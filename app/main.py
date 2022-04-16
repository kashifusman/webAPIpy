from fastapi import FastAPI
# to fetching the column names and converting into dict object
from .routers import post,user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# Once alembic implimented no longer required this , this is for model to table creation manully
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#change origins to array
# origins = ["https://wwww.google.com"]
# now if you add google.com your applciation will alow request from google.com
origins = ["*"]
#this will allow to all

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    return {"message": "Welcome to my first PHP API Kashif>usman"}




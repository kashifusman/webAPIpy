from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
# replace schemas.UserLogin with oauth2passwordrequestform - :?> it save user name instead email

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    login_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    #OAuth2PasswordRequestForm send user name and pwd
    print(login_user)
    if not login_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, login_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data = {"user_id": login_user.id})
    # creata a token 
    # return token
    return {'access_token': access_token, "token_type": "bearer"}
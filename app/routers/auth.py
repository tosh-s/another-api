from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas
# need to import session because we will fetch the user details from the DB
from .. import database, oauth2
from .. import models, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model= schemas.Token)
# after importing the oauthpasswordrequestform, alternate implementation was used.
# def login(user_credentials: schemas.UserLogin, db:Session = Depends(database.get_db)):
#   user = db.query(models.User).filter(models.User.email==user_credentials.email).first()

# alternate implementation. the = Depends() sets up a dependency.
# Oauthpasswordrequestform returns the user details as username/password and not email/password.
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()



    if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User not found")

# if incorrect user details then error      
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

# if user details correct, then at this stage create a token and return a token. This fxn is defined in oauth2.py file.
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}





from ast import Str
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
# from requests import Session
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

#1 this variable uses a function to grab the token from the user login operation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

#secret_key
#algorithm
#expiration time

## changed at 9:20 to use the settings object. the values are moved to the env.py file
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

## create a fxn, that takes a dict input
def create_access_token(data: dict): 
    to_encode = data.copy()

## using the token expiration time specified, update the expiration time.
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

## remember we talked about token signature consisting of a header, user data - payload and secret. 
## All 3 are hashed with an algorithm to get the signature i.e encoded jwt.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#3 this is called by #2 after the token is grabbed from #1. this fxn contains logic to verify token
def verify_access_token(token: str, credentials_exception):    
    try: 
# decode the token first.
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
# remember that we are using the id in the bearer token in the auth.py file. 
# create a new str var and set it equal to user_id of the payload.
        id: str = payload.get("user_id")

# if no id is found in the token raise error or else create var token_data
        if id is None:
            raise credentials_exception

        token_data =schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    return token_data

# this fxn uses the token from #1 above and puts it into anther fxn #3 to verify the token
# what have we done - anytime the user tries to access a protected endpoint, eg crearting a post, 
""" def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials", 
    headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception) """
# we can add a dependency to the function that follows the decorator for that action in the main file. 
# eg add dependency to def create_post and add depends(outh2.getcurrent_user)


## this is 2 i.e. alternate implementation of get_current_user to query db with user id.
# import database, import session, import models
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials", 
    headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
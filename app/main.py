from distutils.log import error
from logging import raiseExceptions
from multiprocessing import synchronize
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, validator, BaseSettings
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
from . import models, schemas, utils 
from .database import engine, get_db
import time
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

## Commented out this line at 11:17 after alembic because SQLAlchemy autogeneration is not needed.
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# reference the router object, aka wiring up the router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Moved this code to schemas.py after ORM section
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    ## rating: Optional[int] = None  ##later made optional after setting up postgres


try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='calgary',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("database connection was successfull!")
except Exception as error:
    print("connecting to database failed")
    print("Error:",error)
from ast import Delete
from enum import unique
from tkinter import CASCADE
from sqlalchemy.sql.expression import null, text
from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

## every model is a table in our database, created and CRUDed by SQLAlchemy
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#   added this code at 8:00 
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
#   added a rel to the user table, i.e. retrieving a post will auto fetch the user info for us
    owner = relationship("User")    

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique = True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = 'votes'
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key = True)
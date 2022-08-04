from pyexpat import model
from orm import String
from sqlalchemy import func
from app import oauth2
from .. import models, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db

# the idea here is that since the code is separated from the app
# app will refer to router and router will refer to the correct decorator 
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# query parameters at 8:40 modify path operation
# add a prefix to the router object and remove /posts from the decorator to simplify the path
#@router.get("/", response_model=List[schemas.Post])
@router.get("/")
#MEthod B uses python ORM
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#    posts = db.query(models.Post).all()
#query parameters
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit: int = 10, search: Optional[str]=""):
# Line below was commented at 10:16 while doing Join to get Votes on Posts.
#    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
# commented line below will only get posts created by that user.
#    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#    return {"data": posts}
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
#     print (posts)
#     return posts

    #results = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
#    print (results)
    return results

@router.get("/newposts")
def get_newpost():
    return {"data": "This is a new post"}



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# using Method B. added oauth2 dependency at 7:24
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
#    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
# Method B
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#        modified at 10:28 to include votes in the response
#        post = db.query(models.Post).filter(models.Post.id==id).first()
        post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id==id).first()
        print(post)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
#        return {"post_detail": post}
        return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# Method B is inserted here
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    # my_posts.pop(index)
    ##return{"message": "post was successfully deleted"}
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id: {id} not found") # alternate way of error handling

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail= f"you cannot delete other users posts") # alternate way of error handling

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_posts(id: int, post: Post):
#     index = get_post_index(id)

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail= f"post with id: {id} not found")

#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return{"data": post_dict}

@router.put("/{id}", status_code=status.HTTP_200_OK)
# Method B is given below
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    # if updated_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail= f"you cannot update other users posts") # added at 8:21 

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
#    return{"data": post_query.first()}
    return post_query.first()

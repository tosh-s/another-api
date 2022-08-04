from .. import models, schemas, database, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db

# the idea here is that since the code is separated from the app
# app will refer to router and router will refer to the correct decorator 
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"user{current_user.id} has already voted on post {vote.post_id}")
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id =current_user.id)
            db.add(new_vote)
            db.commit()
            return{"message": "successfully added vote"}
    else:       
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post doesn't exist")


        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
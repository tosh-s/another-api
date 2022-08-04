from .. import models, schemas, utils 
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# A/C creation validation path, note the response model is specified.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# using Method B pass the schema in the fxn arg
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    # update the pydantic user model password field.
    user.password = hashed_password
#  define a new variable and set it to the model data sent as unpacked dict object
    new_user = models.User(**user.dict())
    # operations to add unpacked dict data to the DB table
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# note that the response is always specified in the decorator
# note that we reduced the route length by using a prefix in the route object above
@router.get('/{id}', response_model=schemas.UserOut)
# Method B
def get_user(id: int, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id==id).first()
        print(user)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} was not found")
#        return {"post_detail": post}
        return user

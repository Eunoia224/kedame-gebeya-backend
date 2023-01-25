from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import Optional, List

# the router object
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturnModel)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ a function to create a user.

    Args:
        user (schemas.UserCreate): our schema.
        db (Session, optional): The session we create. Defaults to Depends(get_db).
    """
    hashed_password = utils.hash(user.password)
    user.password =hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserReturnModel)
def get_user(id: str, db: Session = Depends(get_db)):
    """Get a single user using their id.

    Args:
        id (int): The unique identifier that is assigned when registering.
        db (Session, optional): The Session we create. Defaults to Depends(get_db).
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found.")
    return user


@router.get("/", response_model=List[schemas.UserReturnModel])
def get_users(db: Session = Depends(get_db)):
    """Get all users.

    Args:
        db (Session, optional): The Session we create. Defaults to Depends(get_db).
    """
    users = db.query(models.User).all()
    return users


# TODO let user be updated
# @router.put("/{id}")
# # posts: Post to make sure the frontend sends the right schema (format of data)
# def update_product(id: str, updated_user: schemas.UserCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
#     """Updates a product with the provided id.

#     Args:
#         id (int): the unique number that is assigned to all products when creating them.
#         product (Product): extension of the Product class.
#     """

#     user_query = db.query(models.User).filter(models.User.id == id)
#     user = user_query.first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"user with id: {id} was not found")
#     user_query.update(updated_user.dict(), synchronize_session=False)
#     db.commit()
#     return user_query.first()

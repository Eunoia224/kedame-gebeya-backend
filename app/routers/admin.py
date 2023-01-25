from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import Optional, List

# the router object
router = APIRouter(
    prefix="/super",
    tags=["Super Admins"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SuperAdminReturnModel)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    """ a function to create a super admin.

    Args:
        user (schemas.UserCreate): our schema.
        db (Session, optional): The session we create. Defaults to Depends(get_db).
    """
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    new_admin = models.SuperAdmin(**admin.dict())
    if db.query(models.User).filter(models.User.email == new_admin.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"This email is being used by someone else")
    else:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin


@router.get("/{id}", response_model=schemas.SuperAdminReturnModel)
def get_admin(id: str, db: Session = Depends(get_db)):
    """Get a single admin using their id.

    Args:
        id (int): The unique identifier that is assigned when registering.
        db (Session, optional): The Session we create. Defaults to Depends(get_db).
    """
    Admin = db.query(models.SuperAdmin).filter(
        models.SuperAdmin.id == id).first()
    if not Admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} was not found.")
    return Admin


@router.get("/", response_model=List[schemas.SuperAdminReturnModel])
def get_admin(db: Session = Depends(get_db)):
    """Get all admins.

    Args:
        db (Session, optional): The Session we create. Defaults to Depends(get_db).
    """
    admin = db.query(models.SuperAdmin).all()
    return admin


# TODO let user be updated
@router.put("/{id}")
# posts: Post to make sure the frontend sends the right schema (format of data)
def update_product(id: str, updated_user: schemas.UserCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """Updates a product with the provided id.

    Args:
        id (int): the unique number that is assigned to all products when creating them.
        product (Product): extension of the Product class.
    """

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

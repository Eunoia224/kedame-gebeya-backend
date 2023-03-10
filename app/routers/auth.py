from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Handles the authentication of users for login.

    Args:
        user_credentials (schemas.LoginModel): the data that is provided by the user.
        db (Session, optional): our Session. Defaults to Depends(get_db).
    """
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.email == user_credentials.username).first()
    if not user or admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid, User Not Found.")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password."
        )
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

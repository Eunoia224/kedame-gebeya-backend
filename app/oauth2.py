from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings


oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key

HASH_ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.access_token_expiration_minutes


def create_access_token(data: dict):
    # we don't necessarily need to copy data but we are doing so to prevent any
    # accidental change to the data
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    """Verify the access token with the token provided by the user. 

    Args:
        token (str): the generated token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    """Pass it to any path operation as a dependency and this will get the token
    from the request automatically and extract the ID, verify the token by
    calling `verify_access_token()` and can also fetch the user from the
    database to add it to our path operation as parameter. """
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Couldn't validate credential.", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user


def get_admin(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Couldn't validate credential.", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.id == token.id).first()
    return admin

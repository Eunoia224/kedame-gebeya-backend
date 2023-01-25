from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# the pydantic model


class ProductBase(BaseModel):
    # TODO if you encounter an error for the id exists and can't create the
    # product
    # id: str
    product_name: str
    main_img: str
    img_1: str
    img_2: str
    img_3: str
    img_4: str
    img_5: str
    img_6: str
    img_7: str
    category: str
    manufacturer: str
    weight: float
    items_included: str
    type_of_item: str
    price: int
    detail: str
    stock_quantity: int
    sale: bool = False
    sale_price: int
    review_stars: int
    reviews: str


class ProductCreate(ProductBase):
    pass


class UserCreate(BaseModel):
    """handles the creation of users."""
    first_name: str
    last_name: str
    delivery_address: str
    email: EmailStr
    phone_number: int
    password: str


class UserReturnModel(BaseModel):
    """Handles the response (the data) that is sent when a user is created."""
    id: str
    first_name: str
    last_name: str
    delivery_address: str
    email: EmailStr
    phone_number: int
    created_at: datetime

    class Config:
        """pydantic orm_mode will tell the pydantic model to read the data even if it is not a `dict` but an ORM model."""
        orm_mode = True


class ReviewCreate(BaseModel):
    """handles the creation of a review."""
    # id: str
    # user_id: str
    # product_id: str
    comment: str
    stars: int
    # created_at: datetime



class ReviewReturnModel(BaseModel):
    id: str
    user_id: str
    product_id: str
    comment: str
    stars: int

    class Config:
        """pydantic orm_mode will tell the pydantic model to read the data even if it is not a `dict` but an ORM model."""
        orm_mode = True


class AdminCreate(BaseModel):
     id: str
     first_name: str
     last_name: str
     email: EmailStr
     phone_number: int
     created_at: datetime


class SuperAdminReturnModel(BaseModel):
    """Handles the response (the data) that is sent when a super admin is created."""
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    created_at: datetime

    class Config:
        """pydantic orm_mode will tell the pydantic model to read the data even if it is not a `dict` but an ORM model."""
        orm_mode = True


class LoginModel(BaseModel):
    """Handles authentication of users for access of the API."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """ Verify the token is valid and also the right format. """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Check the validity of the embedded data."""
    id: Optional[str] = None


class Product(ProductBase):
    # extend PostBase to prevent duplication
    created_at: datetime
    owner_id: str
    owner: UserReturnModel

    class Config:
        """pydantic orm_mode will tell the pydantic model to read the data even if it is not a `dict` but an ORM model."""
        orm_mode = True

# class RateReturn(BaseModel):
#     """Handles the response that is sent out when a user gets posts """
#     Product: Product
#     rate: int
# class Rate(BaseModel):
#     """Check the validity of the embedded data for rating. """
#     product_id: str
#     dir: int

# TODO left at http://localhost:5000/step-15-vote-or-like/#now-using-sqlalchemy

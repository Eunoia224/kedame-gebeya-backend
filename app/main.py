from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
# from random import randrange
# from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, product, auth, admin, reviews
from .config import settings


# TODO don't forget to figure out rating system
# models.Base.metadata.create_all(bind=engine)
# TODO try to use the cors with google
# our fastAPI reference
app = FastAPI()
origins = ["*"]  # [*] (a wildcard to allow all sites)
app.add_middleware(
    CORSMiddleware,
    # allow_origin=origins,  # Specifies which domains can talk to our API
    allow_credentials=True,
    # What methods are allowed for the users (Post, Get, Delete....)
    allow_methods=["*"],
    allow_headers=["*"])


class Product(BaseModel):
    product_name: str
    image_address: str
    category: str
    type_of_item: str
    price: int
    detail: str
    sale: Optional[bool] = False
    sale_price: int
    review_stars: int
    reviews: str


app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(reviews.router)
app.include_router(user.router)
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
from .routers import user, product, auth
from .config import settings

# models.Base.metadata.create_all(bind=engine)

# our fastAPI reference
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origin=origins
    allow_credentials=True,
    allow_methods=["*"]
    allow_headers=["*"]
)

# Temporary block
my_data = [{"id": 1,
            "title": "this is the title of the first post",
            "detail": "this is the content of the first post"},
           {"id": 1,
            "title": "this is the title of the second post",
            "detail": "this is the content of the second post"}]


def find_product(id):
    for p in my_data:
        if p["id"] == id:
            return p


def find_product_index(id):
    for i, product in enumerate(my_data):
        if product["id"] == id:
            return i


try:
    conn = psycopg2.connect(host="localhost", database="kedame_gebeya",
                            user="postgres", password="shitgotreal", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    # print("Connected.")
except Exception as error:
    print("Couldn't connect to the server.")
    print("Error: ", error)
# Temporary block ends


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


app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
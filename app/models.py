import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
import uuid


class Product(Base):
    """The model to define the structure of our product table.

    Args:
        Base (_type_): the session
    """
    __tablename__ = "products"
    # id = Column(String, primary_key=True, nullable=False, default=generate_id_for_product)
    id = Column(String, primary_key=True, nullable=False, default=lambda: uuid.uuid4().hex)
    product_name = Column(String, index=True, nullable=False)
    # image_address = Column(String, nullable=False)
    main_img = Column(String, nullable=False)
    img_1 = Column(String, nullable=False)
    img_2 = Column(String, nullable=False)
    img_3 = Column(String, nullable=False)
    img_4 = Column(String, nullable=False)
    img_5 = Column(String, nullable=False)
    img_6 = Column(String, nullable=False)
    img_7 = Column(String, nullable=False)
    category = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    weight = Column(Float)
    items_included = Column(String)
    type_of_item = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    detail = Column(String, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    sale = Column(Boolean)
    sale_price = Column(Integer)
    review_stars = Column(Integer, default=0)
    reviews = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.datetime.now)
    owner_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    """The model to define the structure for the user table.

    Args:
        Base (_type_): the session
    """
    __tablename__ = "users"
    id = Column(String, primary_key=True, nullable=False,
                default=lambda: uuid.uuid4().hex)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    delivery_address = Column(String)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(Integer, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.datetime.now)
    
    
class SuperAdmin(Base):
    """The model to define our structure for the super admins.

    Args:
        Base (_type_): The session
    """
    __tablename__ = "super_admin"
    id = Column(String, primary_key=True, nullable=False, default=lambda:uuid.uuid4().hex)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(Integer, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.datetime.now)
    
    
class Review(Base):
    """Handles the creation of the rating table."""
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, nullable=False,
                default=lambda: uuid.uuid4().hex)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    comment = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.datetime.now)
    owner = relationship("User")

from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import Optional, List

# the router object
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[schemas.RateReturn])
async def get_products(db: Session = Depends(get_db), limit: int = 0, skip: int = 0, search: Optional[str] = ""):
    """ This is the root of the API."""
    # products?limit=10
    # products?skip=10
    # to chain
    # products?limit=2&skip=10
    print(search)
    # products = db.query(models.Product).filter(
    #     models.Product.product_name.contains(search)).offset(skip).all()
    # in case there is a need to limit the number of product we send
    # products = db.query(models.Product).limit(limit).all()
    # if we need to skip a said number of products (USEFUL FOR pagination)
    # products = db.query(models.Product).offset(skip).all()
    results = db.query(models.Product, func.count(models.Rate.product_id)
                       .label("Ratings")).join(models.Rate, models.Rate
                                               .product_id ==models.Product.id, isouter=True).group_by(models.Product.id).filter(models.Product.product_name.contains(search)).offset(skip).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """Create products.

    Args:
        product (Product): extension of the Product class.

    Returns:
        object: returns an object that contains array of the products.
    """
    new_product = models.Product(owner_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/{id}", response_model=schemas.RateReturn)
def get_product(id: str, response: Response, db: Session = Depends(get_db)):
    """grab a product using it's id.

    Args:
        id (int): the unique number that is assigned to all products when creating them.
    """
    # look through the database and once it finds the first match it stops and execute the SQL
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found.")
    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """deletes a product with the provided id.

    Args:
        id (int): the unique number that is assigned to all products when creating them.
    """
    deleted_product = db.query(models.Product).filter(models.Product.id == id)
    product = deleted_product.first()
    if deleted_product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found.")
    if product.owner_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action (You might not have created this product listing).")

    deleted_product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Product)
# posts: Post to make sure the frontend sends the right schema (format of data)
def update_product(id: str, updated_product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """Updates a product with the provided id.

    Args:
        id (int): the unique number that is assigned to all products when creating them.
        product (Product): extension of the Product class.
    """

    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")
    if product.owner_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action (You might not have created this product listing) .")
    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()

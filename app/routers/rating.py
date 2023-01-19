from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/rate",
    tags=["Rating"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def rate(rate: schemas.Rate, db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.get_current_user)):
    """path for the rate system also checks for the existence of the post and whether the user rated it or not."""
    product = db.query(models.Product).filter(models.Product.id == rate.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id: {rate.product_id} was not found.")
    rate_query = db.query(models.Rate).filter(
        models.Rate.product_id == rate.product_id, models.Rate.user_id == current_user.id)
    found_rate = rate_query.first()
    if rate.dir >= 1:
        if found_rate:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with email {current_user.email} has already rated on product with id: {rate.product_id}.")
        new_rate = models.Rate(product_id = rate.product_id, user_id=current_user.id)
        db.add(new_rate)
        db.commit()
        return {"Message": "Successfully rated"}

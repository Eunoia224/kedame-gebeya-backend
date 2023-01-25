from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import Optional, List

# the router object
router = APIRouter(
    prefix="/review",
    tags=["Review"]
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.ReviewReturnModel)
def create_review(id: str, review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """ a function to create a review.
    

    Args:
        review (schemas.ReviewCreate): our schema.
        db (Session): The session we create. Defaults to Depends(get_db).
    """

    new_review = models.Review(
        user_id=current_user.id, product_id=id, **review.dict())
    product = db.query(models.Review).filter(models.Review.product_id == id).first()
    user = db.query(models.Review).filter(models.Review.user_id == current_user.id).first()
    if product and user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"It appears that you have rated this product.")
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/{id}", response_model=schemas.ReviewReturnModel)
def get_review(id: str, db: Session = Depends(get_db)):
    """Get a single review using the id.

    Args:
        id (int): The unique identifier that is assigned when registering a review.
        db (Session, optional): The Session we create. Defaults to Depends(get_db).
    """
    review = db.query(models.Review).filter(models.Review.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"review with id: {id} was not found.")
    return review


@router.get("/", response_model=List[schemas.ReviewReturnModel])
def get_reviews(db: Session = Depends(get_db)):
    """Get all reviews.

    Args:
        db (Session, optional): The Session we create. Defaults to Depends(get_db).
    """
    review = db.query(models.Review).all()
    return review

@router.put("/{id}")
# posts: Post to make sure the frontend sends the right schema (format of data)
def update_review(id: str, updated_review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """Updates a review with the provided id.

    Args:
        id (int): the unique number that is assigned to all reviews when creating them.
        review (review): extension of the Review class.
    """

    review_query = db.query(models.Review).filter(models.Review.id == id)
    review = review_query.first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"review with id: {id} was not found")
    review_query.update(updated_review.dict(), synchronize_session=False)
    db.commit()
    return review_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """deletes a review with the provided id.

    Args:
        id (int): the unique number that is assigned to all review when creating them.
    """
    deleted_review = db.query(models.Review).filter(models.Review.id == id)
    review = deleted_review.first()
    if deleted_review.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"review with id: {id} was not found.")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action (You might not have created this review).")
    deleted_review.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

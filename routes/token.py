from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.db_queue import get_token,cancel_token


router = APIRouter(
    prefix="/token",
    tags=["token"]
)

@router.get("/{token_id}")
def token(
    token_id:int,
    db: Session = Depends(get_db)
):
    return get_token(
        db,
        token_id
    )

@router.patch("/{token_id}/cancel")
def cancel(
    token_id:int,
    db: Session = Depends(get_db)
):
    return cancel_token(
        db,
        token_id
    )
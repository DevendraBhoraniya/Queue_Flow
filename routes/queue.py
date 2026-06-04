from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.db_queue import create_queue
from database.schemas import QueueBase, QueueResponse
from database.db_user import  get_current_user

router = APIRouter(
    prefix="/queue",
    tags=["queue"]
)

@router.post("/create", response_model=QueueResponse)
def new_queue(
    request: QueueBase,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_queue(
        db,
        request,
        current_user.id
    )
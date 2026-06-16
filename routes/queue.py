from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.db_queue import create_queue, get_queues_all, Join_queue, start_queue, get_queue_by_id , next_serving , get_queues_by_user
from database.schemas import QueueBase, QueueResponse, QueueTokenResponse,QueueTokenBase
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

@router.get("/all", response_model=list[QueueResponse])
def get_all( db: Session = Depends(get_db)):
    return get_queues_all(db)

@router.post('/join', response_model=QueueTokenResponse)
def Join(
    request:QueueTokenBase , 
    db: Session = Depends(get_db),
):
    return Join_queue(
    db,
    request
)

@router.get("/{queue_id}")
def queue(
    queue_id: int,
    db: Session = Depends(get_db)
):
    return get_queue_by_id(
        db,
        queue_id
    )


@router.get("/my")
def my_queues(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_queues_by_user(
        db,
        current_user.id
    )


@router.patch('/{queue_id}/start')
def start(
    queue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return start_queue(
    db,
    queue_id,  
    current_user.id    
    )

@router.patch("/{queue_id}/next")
def next_token(
    queue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return next_serving (
    db,
    queue_id,  
    current_user.id,
    )

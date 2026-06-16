from fastapi import Depends, HTTPException
from sqlalchemy.orm.session import Session
from database.models import Queue, QueueToken
from database.schemas import QueueBase, QueueTokenBase
from database.database import get_db

def create_queue(
    db: Session,
    request: QueueBase,
    user_id: int
):
    existing_queue = (
    db.query(Queue)
    .filter(
        Queue.name == request.name,
        Queue.created_by_id == user_id
    )
    .first()
    )

    if existing_queue:
        raise HTTPException(
            status_code=400,
            detail="Queue already exists"
    )

    new_queue = Queue(
        name=request.name,
        average_service_time=request.average_service_time,
        created_by_id=user_id
    )

    db.add(new_queue)
    db.commit()
    db.refresh(new_queue)

    return new_queue

def get_queues_all(db: Session):
    return db.query(Queue).all()

def get_queues_by_user(db: Session, user_id: int):
    return db.query(Queue).filter(Queue.created_by_id == user_id).all()

def get_queue_by_id(db: Session, queue_id:int):
    return db.query(Queue).filter(Queue.id == queue_id).first()

def get_current_queue(
    db: Session = Depends(get_db),
    queue_id = int
):
    queue = (db.query(Queue).filter(Queue.id == queue_id).first())

    if queue is None:
        raise HTTPException(status_code=401, detail="Queue does not exits")
    
    return queue

def Join_queue(db: Session, request: QueueTokenBase):

    queue = (
        db.query(Queue)
        .filter(Queue.id == request.queue_id)
        .first()
    )

    if queue is None:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    total_tokens = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == request.queue_id
        )
        .count()
    )

    waiting_count= (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == request.queue_id,
            QueueToken.status == 'waiting'
        )
        .count()
    )

    position = waiting_count 
    token = f"A{total_tokens + 1:03d}"

    waiting_count = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == request.queue_id,
            QueueToken.status == "waiting"
        )
        .count()
    )

    estimated_wait_time = (
        (waiting_count + 1)
        * queue.average_service_time
    )

    new_token = QueueToken(
        token=token,
        queue_id=request.queue_id,
        joiner_name=request.joiner_name
    )

    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return {
        "id": new_token.id,
        "token": new_token.token,
        "queue_id": new_token.queue_id,
        "joiner_name": new_token.joiner_name,
        "status": new_token.status,
        "created_at": new_token.created_at,
        "position": position,
        "estimated_wait_time": estimated_wait_time
    }

def start_queue(
    db: Session,
    queue_id: int,
    user_id: int
):

    queue = (
        db.query(Queue)
        .filter(
            Queue.id == queue_id,
            Queue.created_by_id == user_id
        )
        .first()
    )

    if queue is None:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    existing_serving = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == queue_id,
            QueueToken.status == "serving"
        )
        .first()
    )

    if existing_serving:
        raise HTTPException(
            status_code=400,
            detail="Queue already started"
        )

    first_waiting = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == queue_id,
            QueueToken.status == "waiting"
        )
        .order_by(QueueToken.created_at)
        .first()
    )

    if first_waiting is None:
        raise HTTPException(
            status_code=404,
            detail="No waiting customers"
        )

    first_waiting.status = "serving"

    db.commit()
    db.refresh(first_waiting)

    return {
        "message": "Queue started",
        "now_serving": first_waiting.token
    }

def next_serving(
    db: Session,
    queue_id: int,
    user_id: int,
):

    queue = (
        db.query(Queue)
        .filter(
            Queue.id == queue_id,
            Queue.created_by_id == user_id
        )
        .first()
    )

    if queue is None:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    current_serving = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == queue_id,
            QueueToken.status == "serving"
        )
        .first()
    )

    if current_serving:
        current_serving.status = "completed"

    next_waiting = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == queue_id,
            QueueToken.status == "waiting"
        )
        .order_by(QueueToken.created_at)
        .first()
    )

    if next_waiting:
        next_waiting.status = "serving"

    db.commit()

    return {
        "completed": (
            current_serving.token
            if current_serving
            else None
        ),
        "now_serving": (
            next_waiting.token
            if next_waiting
            else None
        )
    }


def get_token(
    db: Session,
    token_id: int,
):
    current_token =(
        db.query(QueueToken)
        .filter(
            QueueToken.id == token_id,
        ).first())

    if current_token is None:
        raise HTTPException(
            status_code=404,
            detail="The Token you are searching is not there please check with correct or not"
        )

    queue = (
        db.query(Queue)
        .filter(
            Queue.id == current_token.queue_id
        )
        .first()
    )

    waiting_before = (
        db.query(QueueToken)
        .filter(
            QueueToken.queue_id == current_token.queue_id,
            QueueToken.status == "waiting",
            QueueToken.created_at < current_token.created_at
        )
        .count()
    )

    if current_token.status == "waiting":
        position = waiting_before + 1
        estimated_wait_time = (
            position *
            queue.average_service_time
        )
    else:
        position = 0
        estimated_wait_time = 0

    return{
        "Token_Number":current_token.token,
        "Joiner_name":current_token.joiner_name,
        "status": current_token.status,
        "Position":position,
        "Estimated_waiting_time": estimated_wait_time,
        "Created_at":current_token.created_at
    }
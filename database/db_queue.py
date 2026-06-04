from sqlalchemy.orm.session import Session
from database.db_user import get_current_user
from database.models import Queue
from database.schemas import QueueBase


def create_queue(
    db: Session,
    request: QueueBase,
    user_id: int
):
    new_queue = Queue(
        name=request.name,
        average_service_time=request.average_service_time,
        created_by_id=user_id
    )

    db.add(new_queue)
    db.commit()
    db.refresh(new_queue)

    return new_queue
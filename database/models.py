from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    queues = relationship("Queue", back_populates="created_by")


class Queue(Base):
    __tablename__ = "queues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    average_service_time = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    created_by = relationship("User", back_populates="queues")
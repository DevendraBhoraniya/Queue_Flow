from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    queues = relationship(
        "Queue",
        back_populates="created_by"
    )


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    average_service_time = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_by = relationship( "User",back_populates="queues" )
    queue_tokens = relationship("QueueToken", back_populates="queue", cascade="all, delete-orphan" )

class QueueToken(Base):
    __tablename__ = "queue_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    queue_id = Column( Integer,ForeignKey("queues.id"), nullable=False,index=True)
    joiner_name = Column(String, nullable=False)
    status = Column(
        Enum(
            "waiting",
            "serving",
            "completed",
            "cancelled",
            name="queue_status"
        ),
        default="waiting",
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow )
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    queue = relationship("Queue",back_populates="queue_tokens")



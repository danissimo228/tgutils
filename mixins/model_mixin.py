import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, UUID, DateTime

Base = declarative_base()


class CreatedUpdatedModelMixin(Base):
    """Base model for all models"""
    __abstract__ = True

    id = Column(UUID, primary_key=True, unique=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

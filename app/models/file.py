from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base
from app.models.transaction import Transaction


class File(Base):
    """
    Abstract file database entity
    """

    __tablename__ = "FILE"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    transactions = relationship(Transaction, back_populates="file")

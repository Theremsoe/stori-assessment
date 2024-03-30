from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import DECIMAL, UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

if TYPE_CHECKING:
    # if the target of the relationship is in another module
    # that cannot normally be imported at runtime
    from app.models.file import File


class Transaction(Base):
    """
    Transaction database entity
    """

    __tablename__ = "TRANSACTION"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(Integer, ForeignKey("FILE.id"))
    date = Column(String)
    transaction = Column(DECIMAL(scale=2))
    created_at = Column(DateTime(), default=datetime.now)

    file = relationship("File", back_populates="transactions")

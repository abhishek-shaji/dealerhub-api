import uuid
from datetime import date

from sqlalchemy import Column, UUID, String, Boolean, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    registration_number = Column(String, index=True, nullable=False)
    vin_number = Column(String, index=True, nullable=False, unique=True)
    is_new = Column(Boolean, nullable=False, default=False)
    kms_driven = Column(Integer, nullable=False)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=False)
    brand = relationship("Brand", foreign_keys=[brand_id])
    model = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    first_registration = Column(Date, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", foreign_keys=[created_by_id])

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = relationship("User", foreign_keys=[updated_by_id]) 
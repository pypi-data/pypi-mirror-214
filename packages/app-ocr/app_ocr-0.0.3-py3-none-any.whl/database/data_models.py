from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, BINARY
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class FaceModel(Base):
    __tablename__ = 'face_scan_service'
    id = Column(UUID(as_uuid=True), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ImageModel(Base):
    __tablename__ = 'image_scan_service'
    id = Column(UUID(as_uuid=True), primary_key=True)
    image_base64 = Column(String)
    metadata_ = Column('metadata', JSON)
    face_id = Column(UUID(as_uuid=True), ForeignKey('face_scan_service.id'))
    embedded_image = Column(BINARY)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
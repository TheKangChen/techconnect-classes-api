from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from techconnect_classes_api.database.db import Base


class AdditionalMaterial(Base):
    __tablename__ = "additional_materials"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    url = Column(String, nullable=False)

    course = relationship("Course", back_populates="additional_materials")

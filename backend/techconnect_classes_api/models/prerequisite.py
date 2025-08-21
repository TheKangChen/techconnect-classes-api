from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer

from techconnect_classes_api.database.db import Base


class Prerequisite(Base):
    __tablename__ = "prerequisites"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    prereq_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    course = relationship("Course", back_populates="prereqs", foreign_keys=[course_id])
    prereq_course = relationship(
        "Course", back_populates="is_prereq_for", foreign_keys=[prereq_id]
    )

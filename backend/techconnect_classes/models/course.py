from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Text

from techconnect_classes.database.db import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    format_id = Column(Integer, ForeignKey("formats.id"), nullable=False)

    level = relationship("Level", back_populates="courses")
    format = relationship("Format", back_populates="courses")
    handouts = relationship("Handout", back_populates="course")
    additional_materials = relationship("AdditionalMaterial", back_populates="course")

    prereqs = relationship(
        "Prerequisite", foreign_keys="Prerequisite.course_id", back_populates="course"
    )
    is_prereq_for = relationship(
        "Prerequisite",
        foreign_keys="Prerequisite.prereq_id",
        back_populates="prereq_course",
    )

    courses_in_series = relationship("CourseSeries", back_populates="course")
    courses_taken_by_users = relationship("CourseTaken", back_populates="course")

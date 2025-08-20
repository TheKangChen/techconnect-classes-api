from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from techconnect_classes.database.db import Base


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    series_name = Column(String, nullable=False, unique=True)

    courses = relationship("CourseSeries", back_populates="series")
    users_interested = relationship("SeriesInterested", back_populates="series")


class CourseSeries(Base):
    __tablename__ = "course_series"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"), primary_key=True)

    course = relationship("Course", back_populates="courses_in_series")
    series = relationship("Series", back_populates="courses")

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from techconnect_classes.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    courses_taken = relationship("CourseTaken", back_populates="user")
    series_interested = relationship("SeriesInterested", back_populates="user")


class CourseTaken(Base):
    __tablename__ = "courses_taken"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    user = relationship("User", back_populates="courses_taken")
    course = relationship("Course", back_populates="courses_taken_by_users")


class SeriesInterested(Base):
    __tablename__ = "series_interested"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"), primary_key=True)

    user = relationship("User", back_populates="series_interested")
    series = relationship("Series", back_populates="users_interested")

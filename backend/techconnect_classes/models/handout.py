from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR, Integer, String

from techconnect_classes.database.base_class import Base


class Handout(Base):
    __tablename__ = "handouts"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    language_code = Column(
        CHAR(length=2), ForeignKey("languages.language_code"), nullable=False
    )
    url = Column(String, nullable=False)

    course = relationship("Course", back_populates="handouts")
    language = relationship("Language", back_populates="handouts")

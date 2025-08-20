from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from techconnect_classes.database.db import Base


class Format(Base):
    __tablename__ = "formats"

    id = Column(Integer, primary_key=True)
    format_name = Column(String, nullable=False, unique=True)

    courses = relationship("Course", back_populates="format")

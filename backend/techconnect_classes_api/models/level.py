from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from techconnect_classes_api.database.db import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    level_name = Column(String, nullable=False, unique=True)

    courses = relationship("Course", back_populates="level")

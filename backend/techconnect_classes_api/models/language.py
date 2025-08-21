from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR, String

from techconnect_classes_api.database.db import Base


class Language(Base):
    __tablename__ = "languages"

    language_code = Column(CHAR(length=2), primary_key=True)
    language_name = Column(String, nullable=False, unique=True)

    handouts = relationship("Handout", back_populates="language")

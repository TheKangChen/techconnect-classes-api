import logging
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from techconnect_classes_api.database.db import ModelType

log = logging.getLogger(__name__)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType) -> None:
        self.model = model

    def get(self, db: Session, *args, **kwargs) -> Optional[ModelType]:
        log.debug(f"Retrieving one record from {self.model.__name__}")
        return db.query(self.model).filter(*args).filter_by(**kwargs).first()

    def get_multiple(
        self, db: Session, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> Optional[list[ModelType]]:
        log.debug(
            f"Retrieving {limit} records from {self.model.__name__} offset {offset}"
        )
        return (
            db.query(self.model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def insert(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        log.debug(f"Inserting record for {self.model.__name__}: {obj_in.model_dump()}")
        obj_in_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        log.debug(
            f"Updating record for {self.model.__name__} with {obj_in.model_dump()}"
        )
        obj_update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType | None:
        obj = db.query(self.model).get(id)
        log.debug(f"Deleting record from {self.model.__name__} with {obj}")
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    # TODO: Add user CRUD operations

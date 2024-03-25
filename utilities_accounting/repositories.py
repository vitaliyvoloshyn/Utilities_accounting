from typing import Type, List, Union, Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from utilities_accounting.models import Base, Category, Counter

from sqlalchemy.orm.session import sessionmaker


class BaseRepository:
    session = get_db().get_session()

    def __init__(self,
                 model: Type[Base],
                 dto_read_model: Type[BaseModel],
                 dto_add_model: Optional[Type[BaseModel]] = None,
                 dto_rel_model: Type[BaseModel] = None,
                 ):
        self.orm_model = model
        self.dto_read_model = dto_read_model
        self.dto_rel_model = dto_rel_model
        self.session = self.__class__.session()

    @staticmethod
    def context_session(session):
        """Декоратор, який відкриває сессію в контекстному менеджері для функцій репозиторію"""
        def inner_func(func: callable):
            def wrapper(*args):
                with session() as conn:
                    func(*args, conn)
            return wrapper
        return inner_func

    def get_object_by_id(self, pk: int, model: Type[Base] = None, model_dto: Type[BaseModel] = None):
        if not model:
            model = self.orm_model
        if not model_dto:
            model_dto = self.dto_read_model
        orm_obj = self.session.execute(select(model).where(model.id == pk)).scalar()
        return self._model_validate(orm_obj, model_dto)

    def get_list_objects(self, model: Type[Base] = None, model_dto: Type[BaseModel] = None):
        if not model:
            model = self.orm_model
        if not model_dto:
            model_dto = self.dto_read_model
        list_obj_orm = self.session.execute(select(model)).scalars().all()
        return self._model_validate(list_obj_orm, model_dto)

    def get_list_objects_without_relation(self, dto_model: Type[BaseModel]):
        list_obj_orm = self.session.execute(select(self.orm_model)).scalars().all()
        return self._model_validate(list_obj_orm, dto_model)

    def add_counter(self, counter: Type[BaseModel], category_id: int):
        category_orm = self.session.execute(select(Category).where(Category.id == category_id)).scalar()
        counter_orm = Counter(**counter.dict())
        counter_orm.categories.append(category_orm)
        self.session.add(counter_orm)
        self.session.commit()

    def get_list_objects_another_model(self, model: Base, dto_model: BaseModel):
        list_obj_orm = self.session.execute(select(model)).scalars().all()
        return self._model_validate(list_obj_orm, dto_model)

    @staticmethod
    def _model_validate(orm_obj, dto_model) -> Union[BaseModel, List[BaseModel]]:
        if isinstance(orm_obj, list):
            return [dto_model.model_validate(row, from_attributes=True) for row in orm_obj]
        return dto_model.model_validate(orm_obj, from_attributes=True)

    @context_session(session)
    def add_object(self, dto_model: BaseModel, session=None):
        orm_obj = self.orm_model(**dto_model.dict())
        session.add(orm_obj)
        session.commit()


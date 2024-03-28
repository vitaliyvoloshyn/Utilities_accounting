from typing import Type, List, Union, Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from database import get_db
from utilities_accounting.models import Base, Category, Counter, Currency
from sqlalchemy.orm.session import sessionmaker

from utilities_accounting.schemas import CurrencyDTO, CurrencyAddDTO, CurrencyRelDTO


class BaseRepository:
    """Надає базові CRUD-операції.
    Відповідає за валідацію моделей в схеми і навпаки та взаємодію в ORM"""
    session = get_db().get_session()

    def __init__(self,
                 model: Type[Base],
                 dto_read_model: Type[BaseModel],
                 dto_add_model: Type[BaseModel],
                 dto_rel_model: Optional[Type[BaseModel]] = None,
                 ):
        self.orm_model = model
        self.dto_read_model = dto_read_model
        self.dto_rel_model = dto_rel_model
        self.dto_add_model = dto_add_model

    # @staticmethod
    # def context_session(session: sessionmaker):
    #     """Декоратор, який відкриває сессію в контекстному менеджері для функцій репозиторію"""
    #
    #     def inner_func(func: callable):
    #         def wrapper(*args):
    #             with session() as conn:
    #                 func(*args, conn)
    #         return wrapper
    #     return inner_func

    def get_object_by_id(self, pk: int, with_relation: bool = False, validate: bool = True):
        return self.session_get(with_relation=with_relation, pk=pk, validate=validate)

    def get_object_list(self, with_relation: bool = False):
        return self.session_get(with_relation=with_relation)

    def add_object(self, data: dict):
        dto_model = self.validate_dict_to_schema(data)
        self.session_add(dto_model)

    # @staticmethod
    # def _model_validate(orm_obj, dto_model) -> Union[BaseModel, List[BaseModel]]:
    #     if isinstance(orm_obj, list):
    #         return [dto_model.model_validate(row, from_attributes=True) for row in orm_obj]
    #     return dto_model.model_validate(orm_obj, from_attributes=True)

    # @context_session(session)
    # def add(self, dto_model: BaseModel, session=None):
    #     orm_obj = self.orm_model(**dto_model.dict())
    #     session.add(orm_obj)
    #     session.commit()

    #     __________________________________________
    def session_add(self, dto_model: BaseModel):
        """Додання об'єкта в БД. На вхід приймає провалідовану модель (схему)"""
        with self.session() as session:
            self.orm_model(**dto_model.dict())
            session.add(self.orm_model(**dto_model.dict()))
            session.commit()

    def session_get(self, with_relation: bool, validate: bool = True, pk: Optional[int] = None):
        """Витягує дані з таблиці БД. Якщо вказаний id - повертає один запис, якщо не вказаний - список"""
        dto_model = self.dto_read_model
        if with_relation:
            dto_model = self.dto_rel_model
        with self.session() as session:
            if pk:
                obj_orm = session.execute(select(self.orm_model).where(self.orm_model.id == pk)).scalar()
            else:
                obj_orm = session.execute(select(self.orm_model)).scalars().all()
            if validate:
                return self.validate_orm_to_schema(obj_orm, dto_model)
            return obj_orm

    def session_update(self, values: dict):
        with self.session() as session:
            session.execute(update(self.orm_model).values(**values))

    # def __session_get_with_join(self, join_model: Base,pk: Optional[int] = None):
    #     """Витягує дані з таблиці БД. Якщо вказаний id - повертає один запис, якщо не вказаний - список"""
    #     with self.session() as session:
    #         if pk:
    #             obj_orm = session.execute(select(self.orm_model).join(join_model).where(self.orm_model.id == pk)).scalar()
    #         else:
    #             obj_orm = session.execute(select(self.orm_model)).join(join_model).scalars().all()
    #         return self.__validate_orm_to_schema(obj_orm, self.dto_read_model)

    def validate_dict_to_schema(self, data: dict) -> BaseModel:
        """Відповідає за валідацію даних в схему. На вхід приймає словник"""
        return self.dto_add_model.model_validate(data)

    @staticmethod
    def validate_orm_to_schema(orm_model: Base, dto_model: Type[BaseModel]) -> BaseModel | List[BaseModel]:
        """Відповідає за валідацію даних ORM в схему. На вхід приймає модель або список моделей ORM.
        Повертає схему"""
        if not orm_model:
            return None
        if isinstance(orm_model, list):
            return [dto_model.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model.model_validate(orm_model, from_attributes=True)

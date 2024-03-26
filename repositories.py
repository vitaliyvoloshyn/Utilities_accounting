from typing import Type, List, Union, Optional

from pydantic import BaseModel
from sqlalchemy import select

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

    @staticmethod
    def context_session(session: sessionmaker):
        """Декоратор, який відкриває сессію в контекстному менеджері для функцій репозиторію"""

        def inner_func(func: callable):
            def wrapper(*args):
                with session() as conn:
                    func(*args, conn)

            return wrapper

        return inner_func

    def get_object_by_id(self, pk: int):
        return self.__session_get(pk)

    def get_list_objects(self):
        return self.__session_get()

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
    def add(self, dto_model: BaseModel, session=None):
        orm_obj = self.orm_model(**dto_model.dict())
        session.add(orm_obj)
        session.commit()

    #     __________________________________________
    def __session_add(self, dto_model: Type[BaseModel]):
        """Додання об'єкта в БД. На вхід приймає провалідовану модель (схему)"""
        with self.session() as session:
            session.add(**dto_model.dict())
            session.commit()

    def __session_get(self, pk: Optional[int] = None):
        """Витягує дані з таблиці БД. Якщо вказаний id - повертає один запис, якщо не вказаний - список"""
        with self.session() as session:
            if pk:
                obj_orm = session.execute(select(self.orm_model).where(self.orm_model.id == pk)).scalar()
            else:
                obj_orm = session.execute(select(self.orm_model)).scalars().all()
            return self.__validate_orm_to_schema(obj_orm, self.dto_read_model)

    # def __session_get_with_join(self, join_model: Base,pk: Optional[int] = None):
    #     """Витягує дані з таблиці БД. Якщо вказаний id - повертає один запис, якщо не вказаний - список"""
    #     with self.session() as session:
    #         if pk:
    #             obj_orm = session.execute(select(self.orm_model).join(join_model).where(self.orm_model.id == pk)).scalar()
    #         else:
    #             obj_orm = session.execute(select(self.orm_model)).join(join_model).scalars().all()
    #         return self.__validate_orm_to_schema(obj_orm, self.dto_read_model)

    def __validate_dict_to_schema(self, data: dict) -> Type[BaseModel]:
        """Відповідає за валідацію даних в схему. На вхід приймає словник"""
        pass

    @staticmethod
    def __validate_orm_to_schema(orm_model: Base, dto_model: Type[BaseModel]) -> BaseModel | List[BaseModel]:
        """Відповідає за валідацію даних ORM в схему. На вхід приймає модель або список моделей ORM.
        Повертає схему"""
        if not orm_model:
            return None
        if isinstance(orm_model, list):
            return [dto_model.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model.model_validate(orm_model, from_attributes=True)

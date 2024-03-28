from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, joinedload

from repositories import BaseRepository
from utilities_accounting.models import Currency, Unit, Counter, Category, Base
from utilities_accounting.schemas import CurrencyDTO, CurrencyAddDTO, CurrencyRelDTO, UnitDTO, UnitAddDTO, CounterDTO, \
    CounterAddDTO, CategoryDTO, CategoryAddDTO, CounterRelDTO, CategoryCounterRelDTO, CategoryRelDTO


class CurrencyRepository(BaseRepository):
    ...


class UnitRepository(BaseRepository):
    ...


class CounterRepository(BaseRepository):
    def add_object(self, data: dict):
        categories_id = data.get('category_id')
        categories_dto = [category_repository.get_object_by_id(category_id, validate=False) for category_id in categories_id]
        counter_dto = self.get_object_by_id(data.get('counter_id'), validate=False)
        print(counter_dto)
        unit_dto = unit_repository.get_object_by_id(data.get('unit_id'), validate=False)
        counter_dto.unit = unit_dto
        counter_dto.categories.extend(categories_dto)
        # counter_orm = Counter(**counter_dto.dict())
        # categories_orm = [Category(**category.dict()) for category in categories_dto]
        # unit_orm = Unit(**unit_dto.dict())
        # counter_orm.categories.extend(categories_orm)
        # counter_orm.unit = unit_orm
        self.session_update(**counter_dto.dict())

    def session_add(self, orm_model: Base):
        with self.session() as session:
            session.add(orm_model)
            session.commit()


class CategoryRepository(BaseRepository):
    ...


category_repository = CategoryRepository(
    model=Category,
    dto_read_model=CategoryDTO,
    dto_add_model=CategoryAddDTO,
    dto_rel_model=CategoryRelDTO,
)

currency_repository = CurrencyRepository(
    model=Currency,
    dto_read_model=CurrencyDTO,
    dto_add_model=CurrencyAddDTO,
)

unit_repository = UnitRepository(
    model=Unit,
    dto_read_model=UnitDTO,
    dto_add_model=UnitAddDTO,
)

counter_repository = CounterRepository(
    model=Counter,
    dto_read_model=CounterDTO,
    dto_add_model=CounterAddDTO,
    dto_rel_model=CounterRelDTO,
)

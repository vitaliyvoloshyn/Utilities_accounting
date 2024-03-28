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
    def update(self, data: dict):

        with self.session() as session:
            new_counter_name = data.get('name')
            unit_id = data.get('unit_id')
            counter_orm = session.execute(select(Counter).where(Counter.id == data.get('counter_id'))).scalar()
            unit_orm = session.execute(select(Unit).where(Unit.id == unit_id)).scalar()
            categories_orm = session.execute(select(Category).where((Category.id.in_(data.get('category_id'))))).scalars().all()
            counter_orm.name = new_counter_name
            counter_orm.unit = unit_orm
            counter_orm.categories = categories_orm
            session.commit()

    def add(self, data: dict):

        with self.session() as session:
            new_counter_name = data.get('name')
            unit_id = data.get('unit_id')
            categories_id = data.get('category_id')
            counter_orm = Counter(name=new_counter_name)
            unit_orm = session.execute(select(Unit).where(Unit.id == unit_id)).scalar()
            categories_orm = session.execute(select(Category).where((Category.id.in_(categories_id)))).scalars().all()
            counter_orm.unit = unit_orm
            counter_orm.categories = categories_orm
            session.add(counter_orm)
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

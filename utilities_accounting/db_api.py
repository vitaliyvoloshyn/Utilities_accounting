from sqlalchemy import select, text, and_
from sqlalchemy.orm import selectinload, joinedload

from database import get_db
from utilities_accounting.models import Category, Provider, Counter, CategoryCounter, Unit
from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, CounterRelDTO, ProviderDTO, ProviderRelDTO, \
    UnitReadDTO

session = get_db().get_session()


def get_category(pk: int, session: session = session):
    query = (
        select(Category)
            .options(selectinload(Category.providers))
            .where(Category.id == pk)
    )
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        print(f"++++-++++++res_orm = {res_orm}")
        res_dto = [CategoryRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        print(res_dto)
        return res_dto


def get_rel_categories(session: session = session):
    query = select(Category)
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [CategoryRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def get_categories(session: session = session):
    query = select(Category)
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [CategoryDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def get_providers(session: session = session):
    query = select(Provider)
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [ProviderRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def get_unit_list(session: session = session):
    query = select(Unit)
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [UnitReadDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto

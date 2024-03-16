from sqlalchemy import select, text, and_
from sqlalchemy.orm import selectinload, joinedload

from database import get_db
from utilities_accounting.models import Category, Provider, Counter, CategoryCounter, Parent
from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, CounterRelDTO, ProviderDTO, ProviderRelDTO

session = get_db().get_session()


def get_category(pk: int, session: session = session):
    # query = (text("""
    #               SELECT *
    # FROM category
    # JOIN category_counter ON category.id = category_counter.category_id
    # JOIN counter ON counter.id = category_counter.counter_id
    # join provider p on p.category_id  = category.id
    # WHERE category.deleted = false AND counter.deleted = false AND category.id = 2 and p.deleted = false;
    #               """
    #               )
    #          )

    # query = text('select * from category;')

    # query = select(Category)

    query = (
        select(Category)
        .options(selectinload(Category.providers))
        .where(Category.id == pk)
    )
    print(f"query = {query}")
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


def remove_parent(pk: int, session: session = session):
    with session() as sess:
        # parent = select(Parent).where(Parent.id==pk)
        # sess.execute(parent).one()
        sess.query(Parent).filter(Parent.id == pk).delete()
        sess.commit()
        return "parent"

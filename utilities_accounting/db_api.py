from sqlalchemy import select, text, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload

from database import get_db
from exceptions import ExistORMObject
from utilities_accounting.models import Category, Provider, Counter, CategoryCounter, Unit, Account, Currency
from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, CounterRelDTO, ProviderDTO, ProviderRelDTO, \
    UnitReadDTO, CategoryAddDTO, CounterAddDTO, CategoryCounterRelDTO, ProviderAddDTO, AccountRelDTO, CurrencyDTO, \
    AccountDTO, AccountAddDTO, CurrencyAddDTO

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


def get_providers_list(session: session = session):
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


def add_category_orm(category: CategoryAddDTO, session: session = session):
    cat = Category(**category.dict())
    with session() as conn:
        conn.add(cat)
        conn.commit()


def add_category_and_counter(category: CategoryAddDTO, counter: CounterAddDTO = None, unit_id: int = None,
                             session: session = session):
    cat = Category(**category.dict())
    with session() as conn:
        unit = conn.execute(select(Unit).where(Unit.id == unit_id)).scalar()
        print(unit)
        if counter:
            counter_orm = Counter(**counter.dict())
            cat.counters.append(counter_orm)
            counter_orm.unit = unit
        conn.add(cat)
        conn.commit()


def add_provider_orm(provider: ProviderAddDTO, category_id: int, session: session = session):
    provider_orm = Provider(**provider.dict())
    with session() as conn:
        category = conn.execute(select(Category).where(Category.id == category_id)).scalar()
        provider_orm.category = category
        conn.add(provider_orm)
        conn.commit()


def get_categories_counters(session: session = session):
    query = select(Category).options(joinedload(Category.counters))
    with session() as conn:
        res_orm = conn.execute(query).unique().scalars().all()
        res_dto = [CategoryCounterRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def get_accounts_list(session: session = session):
    query = select(Account).options(selectinload(Account.provider))
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [AccountRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def get_currency_list(session: session = session):
    """Повертає CurrencyDTO об'єкт без відношень"""
    query = select(Currency)
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [CurrencyDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def add_account_orm(account: AccountAddDTO):
    """Додає о/р в бд"""
    if _exist_account_in_provider(account.provider_id):
        raise ExistORMObject(text='У даного оператора вже є особовий рахунок')
        return
    account_orm = Account(**account.dict())
    with session() as conn:
        conn.add(account_orm)
        conn.commit()


def _exist_account_in_provider(provider_id: int, session: session = session) -> bool:
    """Перевіряє чи є у провайдера о/р"""
    query = select(Account).where(Account.provider_id == provider_id)
    with session() as conn:
        res = conn.execute(query).scalar()
        if res:
            return True
        return False



def add_currency_orm(currency: CurrencyAddDTO):
    """Додає валюту в бд"""
    currency_orm = Currency(**currency.dict())
    with session() as conn:
        conn.add(currency_orm)
        conn.commit()

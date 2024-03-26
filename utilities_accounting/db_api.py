from sqlalchemy import select, text, and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload

from database import get_db
from exceptions import ExistORMObject
from utilities_accounting.models import Category, Provider, Counter, CategoryCounter, Unit, Account, Currency
from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, CounterRelDTO, ProviderDTO, ProviderRelDTO, \
    UnitDTO, CategoryAddDTO, CounterAddDTO, CategoryCounterRelDTO, ProviderAddDTO, AccountRelDTO, CurrencyDTO, \
    AccountDTO, AccountAddDTO, CurrencyAddDTO, UnitAddDTO

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
        print(type(res_orm[0]))
        res_dto = [ProviderRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
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


def get_currency_by_id(pk: int, session: session = session):
    """Повертає CurrencyDTO об'єкт без відношень"""
    query = select(Currency).where(Currency.id == pk)
    with session() as conn:
        res_orm = conn.execute(query).scalar()
        res_dto = CurrencyDTO.model_validate(res_orm, from_attributes=True)
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


def add_currency_orm(currency: CurrencyAddDTO, session: session = session):
    """Додає валюту в бд"""
    currency_orm = Currency(**currency.dict())
    with session() as conn:
        conn.add(currency_orm)
        conn.commit()


def currency_delete_orm(pk: int, session: session = session):
    """Видаляє валюту по id"""
    with session() as conn:
        currency_orm = conn.execute(select(Currency).where(Currency.id == pk)).scalar()
        conn.delete(currency_orm)
        conn.commit()


def currency_update(currency: CurrencyDTO, session: session = session):
    """Оновлення валюти"""
    stmt = update(Currency).where(Currency.id == currency.id).values(**currency.dict())
    with session() as conn:
        conn.execute(stmt)
        conn.commit()


def units_get_list(session: session = session):
    """Повертає UnitReadDTO без відношень
        поля:
        id,
        name"""
    query = select(Unit)
    with session() as conn:
        res_orm = conn.execute(query).scalars().all()
        res_dto = [UnitDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


def unit_add_orm(unit: UnitAddDTO, session: session = session):
    """Додання одиниці вимірювання в БД"""
    unit_orm = Unit(**unit.dict())
    with session() as conn:
        conn.add(unit_orm)
        conn.commit()


def unit_delete_orm(pk: int, session: session = session):
    """Видаляє одиницю вимірювання по id"""
    with session() as conn:
        unit_orm = conn.execute(select(Unit).where(Unit.id == pk)).scalar()
        conn.delete(unit_orm)
        conn.commit()


def unit_get_by_id(pk: int, session: session = session):
    """Повертає UnitReadDTO об'єкт без відношень"""
    query = select(Unit).where(Unit.id == pk)
    with session() as conn:
        res_orm = conn.execute(query).scalar()
        res_dto = UnitDTO.model_validate(res_orm, from_attributes=True)
        return res_dto


def unit_update(unit: UnitDTO, session: session = session):
    """Оновлення одиницю вимірювання"""
    stmt = update(Unit).where(Unit.id == unit.id).values(**unit.dict())
    with session() as conn:
        conn.execute(stmt)
        conn.commit()

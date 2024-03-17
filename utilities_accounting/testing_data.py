from sqlalchemy import insert, text, select
from sqlalchemy.orm import selectinload

from .models import Category, Provider, Indicator, Account, Payment, Tariff, Currency, Counter, CategoryCounter, Unit


# Додаємо валюту
currencies = [
    Currency(name='Українська гривня', code='UAH'),
    Currency(name='Американський долар', code='USD'),
    Currency(name='Євро', code='EUR'),
]

# Додаємо одиниці вимірювання
units = [
    Unit(value='кВт*год'),
    Unit(value='м3'),
]

categories = [
    Category(name="Електропостачання"),
    Category(name="Водопостачання"),
    Category(name="Газоопостачання"),
    Category(name="Теплопостачання"),
    Category(name="ПОЖ"),
    Category(name="Транспортування газу"),
    Category(name="Переробка сміття"),
]

counters = [
    Counter(name='Електролічильник'),
    Counter(name='Лічильник холодної води'),
    Counter(name='Лічильник гарячої води'),
    Counter(name='Газовий лічильник'),
]


counters[0].categories.append(categories[0])
counters[1].categories.append(categories[1])
counters[2].categories.append(categories[1])
counters[3].categories.append(categories[2])
counters[2].categories.append(categories[3])
counters[0].unit = units[0]
counters[1].unit = units[1]
counters[2].unit = units[1]
counters[3].unit = units[1]

indicators = [
    Indicator(value=3587),
    Indicator(value=3690),
    Indicator(value=411),
    Indicator(value=422),
    Indicator(value=713),
    Indicator(value=718),
    Indicator(value=238),
    Indicator(value=240),
    Indicator(value=426),
]

counters[0].indicators.extend(indicators[0:2])
counters[1].indicators.extend(indicators[2:4])
counters[1].indicators.append(indicators[8])
counters[2].indicators.extend(indicators[4:6])
counters[3].indicators.extend(indicators[6:8])


providers = [
    Provider(name="Електромережі", iban="UA32432765498765432976", edrpou="12356789", icon="EK.png",
             site="https://www.ok.koec.com.ua/"),
    Provider(name="Водоканал", iban="UA8644827878777634567", edrpou="78975432", icon="icon2",
             site="https://www.ok.koec.com.ua/"),
    Provider(name="Газові мережі", iban="UA8482956340856789345", edrpou="78975432", icon="naftogaz.jpg",
             site="https://www.ok.koec.com.ua/"),
    Provider(name="ТЕЦ", iban="UA84826839278232789345", edrpou="26493635", icon="icon4",
             site="https://www.ok.koec.com.ua/"),
    Provider(name="ПОЖ", iban="UA84826878232789345", edrpou="74393635", icon="icon5",
             site="https://www.ok.koec.com.ua/"),
    Provider(name="Регіональні мережі", iban="UA67767372382332789345", edrpou="74393635", icon="icon6",
             site="https://www.ok.koec.com.ua/"),
    Provider(name="ТОВ Переробка сміття", iban="UA59253039278232789345", edrpou="83923635", icon="icon7",
             site="https://www.ok.koec.com.ua/"),
]
providers[0].category = categories[0]
categories[1].providers.append(providers[1])
categories[2].providers.append(providers[2])
categories[3].providers.append(providers[3])
categories[4].providers.append(providers[4])
categories[5].providers.append(providers[5])
categories[6].providers.append(providers[6])


def insert_data_in_currency(session):
    stmt = insert(table=Currency).values([
        {'name': 'Українська гривня', 'code': 'UAH'},
        {'name': 'Американський долар', 'code': 'USD'},
        {'name': 'Євро', 'code': 'EUR'},
    ])
    with session() as conn:
        conn.execute(stmt)
        conn.commit()


def insert_data_in_counter(session):
    stmt = insert(table=Counter).values([
        {'name': 'Електролічильник', 'category_id': 1},
        {'name': 'Лічильник холодної води', 'category_id': 2},
        {'name': 'Лічильник гарячої води', 'category_id': 2},
        {'name': 'Лічильник гарячої води', 'category_id': 4},
        {'name': 'Газовий лічильник', 'category_id': 3},
    ])

    with session() as conn:
        conn.execute(stmt)
        conn.commit()


def insert_data_in_indicator(session):
    stmt = insert(table=Indicator).values([
        {"name": "Електролічильник", "value": "4873", "provider_id": "1"},
        {"name": "Лічильник холодної води", "value": "471", "provider_id": "2"},
        {"name": "Лічильник гарячої води", "value": "275", "provider_id": "2"},
        {"name": "Лічильник гарячої води", "value": "275", "provider_id": "4"},
        {"name": "Газовий лічильник", "value": "117", "provider_id": "3"},
    ])
    with session() as conn:
        conn.execute(stmt)
        conn.commit()


def insert_data_in_account(session):
    stmt = insert(table=Account).values([
        {"number": "535345", "balance": "3", "provider_id": "1"},
        {"number": "345345", "balance": "234", "provider_id": "2"},
        {"number": "3453453", "balance": "23", "provider_id": "3"},
        {"number": "935374", "balance": "64", "provider_id": "4"},
        {"number": "549362", "balance": "25", "provider_id": "5"},
        {"number": "93574", "balance": "98", "provider_id": "6"},
        {"number": "498432", "balance": "4", "provider_id": "7"},
    ])
    with session() as conn:
        conn.execute(stmt)
        conn.commit()


def insert_data_in_tariff(session):
    instance_list = [
        Tariff(value=2.64, provider_id=1),
        Tariff(value=2.64, provider_id=2),
        Tariff(value=2.64, provider_id=3),
        Tariff(value=2.64, provider_id=4),
        Tariff(value=2.64, provider_id=5),
        Tariff(value=2.64, provider_id=6),
        Tariff(value=2.64, provider_id=7),
    ]
    with session() as conn:
        conn.add_all(instance_list)
        conn.commit()


def insert_data_in_payment(session):
    instance_list = [
        Payment(value=264, provider_id=1),
        Tariff(value=164, provider_id=2),
        Tariff(value=294, provider_id=3),
        Tariff(value=236, provider_id=4),
        Tariff(value=44, provider_id=5),
        Tariff(value=24, provider_id=6),
        Tariff(value=64, provider_id=7),
    ]
    with session() as conn:
        conn.add_all(instance_list)
        conn.commit()


# def get_tariff(id:int):
#     query = text("select t.value from tariff t join provider p on t.provider_id = p.id where p.name = 'ПОЖ'")
#     with session() as conn:
#         res = conn.execute(query).scalar()
#         print(res)
# def get_categories():
#     query = select(Indicator).options(selectinload(Indicator.provider)).limit(2)
#     with session() as conn:
#         result = conn.execute(query)
#         result_orm = result.scalars().all()
#         print(f"11 - {result_orm}")
#         result_dto = [IndicatorRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
#         print(result_dto)


def add_data(session):
    with session() as conn:
        conn.add_all(categories)
        conn.add_all(currencies)
        conn.add_all(counters)
        conn.add_all(indicators)
        conn.add_all(providers)
        conn.commit()
    # insert_data_to_category(session)
    # insert_data_in_provider(session)
    # insert_data_in_currency(session)
    # insert_data_in_counter(session)
    # insert_data_in_indicator(session)
    # insert_data_in_account(session)
    # insert_data_in_tariff(session)
    # insert_data_in_payment(session)
    # get_tariff(1)
    # get_categories()


def my_select(session):
    query = select(Category).join(CategoryCounter).where(CategoryCounter.counter_id == 3)
    with session() as conn:
        res = conn.execute(query).scalars().all()
        conn.commit()
        print(res)

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


accounts = [
    Account(number='gf8473938', balance=43.56, provider_id=1, currency_id=1),
    Account(number='vvg567', balance=43.96, provider_id=2, currency_id=1),
    Account(number='hbh7788', balance=67.53, provider_id=3, currency_id=1),
    Account(number='f46', balance=9876.12, provider_id=4, currency_id=1),
    Account(number='876543', balance=432, provider_id=5, currency_id=1),
    Account(number='c3456789', balance=678.4, provider_id=6, currency_id=1),
    Account(number='j5673456', balance=23.4, provider_id=7, currency_id=1),
]

units = [
    Unit(value='кВт*год'),
    Unit(value='м3'),
]



def add_data(session):
    with session() as conn:
        conn.add_all(currencies)
        conn.add_all(units)
        # conn.add_all(categories)
        # conn.add_all(counters)
        # conn.add_all(indicators)
        # conn.add_all(providers)
        # conn.add_all(accounts)
        conn.commit()

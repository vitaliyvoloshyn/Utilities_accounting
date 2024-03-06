from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Provider(Base):
    __tablename__ = "provider"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)
    iban: Mapped[str] = mapped_column(String(29), unique=True, nullable=True)
    edrpou: Mapped[str] = mapped_column(String(8), nullable=True)
    icon: Mapped[str] = mapped_column(nullable=True)
    site: Mapped[str] = mapped_column(nullable=True)
    deleted: Mapped[bool] = mapped_column(server_default='False')
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship(back_populates='providers', cascade='all, delete')
    accounts: Mapped[List['Account']] = relationship(back_populates='provider', cascade='all, delete')
    tariffs: Mapped[List['Tariff']] = relationship(back_populates='provider', cascade='all, delete')

    def __repr__(self) -> str:
        return f"Provider(id={self.id!r}, name={self.name!r})"


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    url_path: Mapped[str] = mapped_column(unique=True)
    deleted: Mapped[bool] = mapped_column(server_default='False')
    providers: Mapped[List["Provider"]] = relationship(back_populates="category", cascade='all, delete')
    counters: Mapped[List['Counter']] = relationship(back_populates='category', cascade='all, delete')

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"


class Counter(Base):
    __tablename__ = 'counter'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    date: Mapped[datetime] = mapped_column(server_default=func.current_date())
    deleted: Mapped[bool] = mapped_column(server_default='False')
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship(back_populates='counters')
    indicators: Mapped[List['Indicator']] = relationship(back_populates='counter')

    def __repr__(self) -> str:
        return f"Indicator(id={self.id!r}, name={self.name!r})"


class Indicator(Base):
    __tablename__ = 'indicator'

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.current_date())
    deleted: Mapped[bool] = mapped_column(server_default='False')
    counter_id: Mapped[int] = mapped_column(ForeignKey('counter.id'))
    counter: Mapped['Counter'] = relationship(back_populates='indicators', cascade='all, delete')

    def __repr__(self) -> str:
        return f"Indicator(id={self.id!r}, value={self.value!r})"


class Account(Base):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str]
    balance: Mapped[float]
    provider_id: Mapped[int] = mapped_column(ForeignKey('provider.id'))
    currency_id: Mapped[int] = mapped_column(ForeignKey('currency.id'))
    deleted: Mapped[bool] = mapped_column(server_default='False')
    provider: Mapped['Provider'] = relationship(back_populates='accounts', cascade='all, delete')
    payments: Mapped[List['Payment']] = relationship(back_populates='account', cascade='all, delete')
    currency: Mapped['Currency'] = relationship(back_populates='accounts', cascade='all, delete')

    def __repr__(self) -> str:
        return f"Account(id={self.id!r}, number={self.number!r})"


class Tariff(Base):
    __tablename__ = 'tariff'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float]
    date: Mapped[datetime] = mapped_column(server_default=func.current_date())
    provider_id: Mapped[int] = mapped_column(ForeignKey('provider.id'))
    provider: Mapped['Provider'] = relationship(back_populates='tariffs', cascade='all, delete')

    def __repr__(self) -> str:
        return f"Tariff(id={self.id!r}, value={self.value!r})"


class Payment(Base):
    __tablename__ = 'payment'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float]
    date: Mapped[datetime] = mapped_column(server_default=func.current_date())
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    account: Mapped['Account'] = relationship(back_populates='payments')

    def __repr__(self) -> str:
        return f"Payment(id={self.id!r}, name={self.value!r})"


class Currency(Base):
    __tablename__ = 'currency'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(String(3))
    accounts: Mapped[List['Account']] = relationship(back_populates='currency')

    def __repr__(self) -> str:
        return f"Currency(id={self.id!r}, name={self.name!r})"

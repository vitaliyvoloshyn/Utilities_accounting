import datetime
from datetime import date
from enum import Enum
from typing import List, Optional, Annotated

from pydantic import BaseModel, Field, validator, field_validator


class CategoryAddDTO(BaseModel):
    name: str


class CategoryDTO(CategoryAddDTO):
    id: int


class CategoryCounterRelDTO(CategoryDTO):
    """view: get_category_list"""
    counters: List["CounterUnitRelDTO"]


class CategoryRelDTO(CategoryCounterRelDTO):
    providers: List["ProviderDTO"]


class ProviderAddDTO(BaseModel):
    name: str
    iban: Optional[str] = None
    edrpou: Optional[str] = Field(max_items=8, min_items=8)
    icon: Optional[str] = None
    site: Optional[str] = None


class ProviderDTO(ProviderAddDTO):
    id: int


class ProviderRelDTO(ProviderDTO):
    """view: get_providers_list"""
    category: "CategoryDTO"


class CounterAddDTO(BaseModel):
    name: str


class CounterDTO(CounterAddDTO):
    id: int


class CounterUnitRelDTO(CounterDTO):
    unit: 'UnitReadDTO'


class CounterRelDTO(CounterDTO):
    indicators: List['IndicatorDTO']


class IndicatorDTO(BaseModel):
    id: int
    value: int = Field(ge=0)
    date: date
    deleted: bool = False
    counter_id: int


class IndicatorRelDTO(IndicatorDTO):
    counter: "CounterDTO"


class AccountAddDTO(BaseModel):
    number: str
    balance: float
    currency_id: int
    provider_id: int


class AccountDTO(AccountAddDTO):
    id: int


class AccountRelDTO(AccountDTO):
    provider: 'ProviderDTO'
    currency: 'CurrencyDTO'


class TariffDTO(BaseModel):
    id: int
    value: float = Field(ge=1)
    date: date
    provider_id: int


class TariffRelDTO(BaseModel):
    provider: 'ProviderDTO'


class PaymentDTO(BaseModel):
    id: int
    value: float = Field(ge=1)
    date: date
    account_id: int


class PaymentRelDTO(BaseModel):
    account: "AccountDTO"


class CurrencyDTO(BaseModel):
    id: int
    name: str
    code: str = Field(min_items=3, max_items=3)


class CurrencyRelDTO(CurrencyDTO):
    accounts: List['CurrencyDTO']


class UnitEnum(Enum):
    ELECTRICITY = 'кВт*год'
    VOLUME = 'м3'


class UnitReadDTO(BaseModel):
    id: int
    value: str


class UnitAddDTO(BaseModel):
    value: UnitEnum

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class CategoryDTO(BaseModel):
    id: int
    name: str
    # url_path: str
    deleted: bool = False


class CategoryRelDTO(CategoryDTO):
    providers: List["ProviderDTO"]
    counters: List["CounterRelDTO"]


class ProviderDTO(BaseModel):
    id: int
    name: str
    iban: Optional[str] = None
    edrpou: Optional[str] = Field(max_items=8, min_items=8)
    icon: Optional[str] = None
    site: Optional[str] = None
    deleted: bool = False
    category_id: int


class ProviderRelDTO(ProviderDTO):
    category: "CategoryDTO"
    accounts: List['AccountDTO']


class CounterDTO(BaseModel):
    id: int
    name: str
    date: date
    deleted: bool = False
    # category_id: int


class CounterRelDTO(CounterDTO):
    # category: 'CategoryDTO'
    indicators: List['IndicatorDTO']


class IndicatorDTO(BaseModel):
    id: int
    value: int = Field(ge=0)
    date: date
    deleted: bool = False
    counter_id: int


class IndicatorRelDTO(IndicatorDTO):
    counter: "CounterDTO"


class AccountDTO(BaseModel):
    id: int
    number: str
    balance: float
    currency_id: int
    provider_id: int
    deleted: bool = False


class AccountRelDTO(AccountDTO):
    provider: 'ProviderDTO'
    payments: List["PaymentDTO"]
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
    accounts: int


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

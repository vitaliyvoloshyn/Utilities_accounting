from repositories import BaseRepository
from utilities_accounting.models import Currency, Unit, Counter
from utilities_accounting.schemas import CurrencyDTO, CurrencyAddDTO, CurrencyRelDTO, UnitDTO, UnitAddDTO, CounterDTO, \
    CounterAddDTO


class CurrencyRepository(BaseRepository):
    ...


class UnitRepository(BaseRepository):
    ...


class CounterRepository(BaseRepository):
    ...


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
)

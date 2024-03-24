from typing import Annotated, Optional

from fastapi import APIRouter, Body, Form, Depends
from fastapi.templating import Jinja2Templates
from pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from exceptions import ExistORMObject
from utilities_accounting.models import Account
from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, UnitAddDTO, CategoryAddDTO, CounterAddDTO, \
    ProviderAddDTO, CurrencyDTO, AccountAddDTO, CurrencyAddDTO, UnitReadDTO, AccountDTO, AccountRelDTO
from utilities_accounting.db_api import get_category, get_rel_categories, get_providers_list, get_categories, \
    add_category_orm, add_category_and_counter, get_categories_counters, add_provider_orm, get_accounts_list, \
    get_currency_list, add_account_orm, add_currency_orm, currency_delete_orm, get_currency_by_id, currency_update, \
    units_get_list, unit_add_orm, unit_delete_orm, unit_get_by_id, unit_update
from utilities_accounting.repositories import BaseRepository

router = APIRouter(prefix='/category', tags=['Main app'])
index_router = APIRouter(tags=['Index'])
admin_router = APIRouter(prefix='/admin', tags=['Admin'])
templates = Jinja2Templates(directory='templates')
account_repo = BaseRepository(model=Account, dto_read_model=AccountDTO, dto_add_model=AccountAddDTO, dto_rel_model=AccountRelDTO)


@index_router.get("/")
async def index(request: Request):
    categories = get_rel_categories()
    return templates.TemplateResponse(name='index.html',
                                      context={
                                          'request': request,
                                          'categories': categories,
                                          'cur_category': []
                                      })


@router.get("/{pk}")
async def category(request: Request, pk: int):
    categories = get_rel_categories()
    cur_category = get_category(pk)[0]
    print(categories)
    return templates.TemplateResponse(name='category.html', context={'request': request,
                                                                     'cur_category': cur_category,
                                                                     'categories': categories})


@index_router.get("/provider/{provider_pk}", name='provider')
async def get_provider(request: Request, provider_pk: int):
    categories = get_rel_categories()

    for pr in category.providers:
        if pr.id == provider_pk:
            provider = pr
    return templates.TemplateResponse(name='service_provider.html', context={'request': request,
                                                                             'cur_category': category,
                                                                             'categories': categories,
                                                                             'cur_provider': provider})


@admin_router.get('/provider')
async def get_providers(request: Request):
    providers = get_providers_list()
    categories = get_categories()
    print(providers)
    return templates.TemplateResponse(name='providers.html', context={'request': request,
                                                                      'cur_category': [],
                                                                      'providers': providers,
                                                                      'categories': categories,
                                                                      })


@admin_router.get('/provider/add')
async def add_category(request: Request):
    categories = get_categories()
    return templates.TemplateResponse(name='add_provider.html', context={'request': request,
                                                                         'cur_category': [],
                                                                         'categories': categories,
                                                                         })


@admin_router.post('/provider/add')
async def add_provider(name: str = Form(),
                       iban: str = Form(),
                       edrpou: str = Form(),
                       site: str = Form(),
                       category_id: int = Form(),
                       ):
    # categories = get_categories()
    provider_dto = ProviderAddDTO.model_validate({
        'name': name,
        'iban': iban,
        'edrpou': edrpou,
        'site': site,
    })
    add_provider_orm(provider=provider_dto, category_id=category_id)
    return RedirectResponse('/admin/provider', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/category')
async def get_category_list(request: Request):
    categories = get_categories_counters()
    return templates.TemplateResponse(name='categories.html', context={'request': request,
                                                                       'cur_category': [],
                                                                       'categories': categories,
                                                                       })


@admin_router.get('/category/add')
async def add_category(request: Request):
    categories = get_categories()
    units = units_get_list()
    return templates.TemplateResponse(name='add_category.html', context={'request': request,
                                                                         'cur_category': [],
                                                                         'categories': categories,
                                                                         'units': units
                                                                         })


@admin_router.post('/category/add')
async def add_category_post(categoryName: str = Form(),
                            counterName: Annotated[str | None, Form()] = None,
                            counterIndicator: Annotated[int | None, Form()] = None,
                            counterUnitId: Annotated[int | None, Form()] = None,
                            categoryIsCounter: Annotated[bool, Form()] = False):
    try:
        category_dto = CategoryAddDTO.model_validate({'name': categoryName})
        counter_dto = None
        if categoryIsCounter:
            counter_dto = CounterAddDTO.model_validate({'name': counterName})

        add_category_and_counter(category=category_dto, counter=counter_dto, unit_id=counterUnitId)
    except IntegrityError as e:
        return {'detail': "Така категорія вже існує"}
    return RedirectResponse('/admin/category', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/account')
async def get_account(request: Request):
    categories = get_categories_counters()
    accounts = account_repo.get_list_objects()
    return templates.TemplateResponse(name='accounts.html', context={'request': request,
                                                                     'cur_category': [],
                                                                     'categories': categories,
                                                                     'accounts': accounts,
                                                                     })


@admin_router.get('/account/add')
async def page_add_account(request: Request):
    """Сторінка додавання особового рахунку"""
    categories = get_categories()
    providers = get_providers_list()
    currencies = get_currency_list()
    return templates.TemplateResponse(name='add_account.html', context={'request': request,
                                                                        'cur_category': [],
                                                                        'categories': categories,
                                                                        'providers': providers,
                                                                        'currencies': currencies,
                                                                        })


@admin_router.post('/account/add')
async def add_account(
        number: str = Form(),
        balance: float = Form(),
        provider_id: int = Form(),
        currency_id: int = Form(),
):
    account_dto = AccountAddDTO.model_validate({
        'number': number,
        'balance': balance,
        'provider_id': provider_id,
        'currency_id': currency_id,
    })
    try:
        add_account_orm(account_dto)
    except ExistORMObject as e:
        return {'detail': e.text}
    return RedirectResponse('/admin/account', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/currency')
def currency_list_view(request: Request):
    """Сторінка зі списком особових рахунків"""
    categories = get_categories()
    currencies = get_currency_list()
    return templates.TemplateResponse(name='currencies.html', context={'request': request,
                                                                       'cur_category': [],
                                                                       'categories': categories,
                                                                       'currencies': currencies,
                                                                       })


@admin_router.get('/currency/add')
def currency_add_page_view(request: Request):
    """Сторінка додавання особового рахунку"""
    categories = get_categories()
    providers = get_providers_list()
    currencies = get_currency_list()
    return templates.TemplateResponse(name='add_currency_form.html', context={'request': request,
                                                                              'cur_category': [],
                                                                              'categories': categories,
                                                                              # 'providers': providers,
                                                                              # 'currencies': currencies,
                                                                              })


@admin_router.post('/currency/add')
def currency_add_post(
        name: str = Form(),
        code: str = Form(),
):
    """POST-запит на додання особового рахунку, передання інформації в БД"""
    currency_dto = CurrencyAddDTO.model_validate({
        'name': name.capitalize(),
        'code': code.upper(),
    })
    try:
        add_currency_orm(currency_dto)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/currency', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/currency/{pk}/delete')
def currency_delete(pk: int):
    """Видалення валюти з БД"""

    try:
        currency_delete_orm(pk)
    except UnmappedInstanceError as e:
        return {'detail': e}
    return RedirectResponse('/admin/currency', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/currency/{pk}/')
def currency_update_form(request: Request, pk: int):
    """Форма редагування валюти"""
    categories = get_categories()
    currency = get_currency_by_id(pk)
    return templates.TemplateResponse(name='currency_update.html', context={'request': request,
                                                                            'cur_category': [],
                                                                            'categories': categories,
                                                                            'currency': currency,
                                                                            })


@admin_router.post('/currency/{pk}/')
def currency_update_form(pk: int, name: str = Form(), code: str = Form()):
    """POST-запит на редагування валюти"""
    try:
        currency_dto = CurrencyDTO.model_validate({
            'id': pk,
            'name': name,
            'code': code.upper(),
        })
    except ValidationError as e:
        return {'detail': e.errors()}

    try:
        currency_update(currency_dto)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/currency', status_code=status.HTTP_303_SEE_OTHER)

# CRUD Unit
# **********************************************************************************************************************
@admin_router.get('/unit')
def unit_list_view(request: Request):
    """Сторінка зі списком одиниць вимірювання"""
    categories = get_categories()
    units = units_get_list()
    return templates.TemplateResponse(name='units.html', context={'request': request,
                                                                  'cur_category': [],
                                                                  'categories': categories,
                                                                  'units': units,
                                                                  })


@admin_router.get('/unit/add')
def unit_add_page_view(request: Request):
    """Сторінка додавання одиниць вимірювання"""
    categories = get_categories()
    return templates.TemplateResponse(name='unit_add_form.html', context={'request': request,
                                                                          'cur_category': [],
                                                                          'categories': categories,
                                                                          })


@admin_router.post('/unit/add')
def unit_add_post(
        value: str = Form(),
):
    """POST-запит на додання одиниці вимірювання, передання інформації в БД"""
    unit_dto = UnitAddDTO.model_validate({'value': value})
    try:
        unit_add_orm(unit_dto)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/unit', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/unit/{pk}/delete')
def unit_delete(pk: int):
    """Видалення одиниці вимірювання з БД"""

    try:
        unit_delete_orm(pk)
    except UnmappedInstanceError as e:
        return {'detail': e}
    return RedirectResponse('/admin/unit', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/unit/{pk}/')
def unit_update_form(request: Request, pk: int):
    """Форма редагування одиниці вимірювання"""
    categories = get_categories()
    unit = unit_get_by_id(pk)
    return templates.TemplateResponse(name='unit_update.html', context={'request': request,
                                                                        'cur_category': [],
                                                                        'categories': categories,
                                                                        'unit': unit,
                                                                        })


@admin_router.post('/unit/{pk}/')
def unit_update_post(pk: int, value: str = Form()):
    """POST-запит на редагування одиниці вимірювання"""
    try:
        unit_dto = UnitReadDTO.model_validate({
            'id': pk,
            'value': value,
        })
    except ValidationError as e:
        return {'detail': e.errors()}

    try:
        unit_update(unit_dto)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/unit', status_code=status.HTTP_303_SEE_OTHER)


# Views Tariff
# **********************************************************************************************************************
@admin_router.get('/tariff')
def tariff_list_view(request: Request):
    """Сторінка зі списком тарифів"""
    categories = get_categories()
    tariffs = units_get_list()
    return templates.TemplateResponse(name='units.html', context={'request': request,
                                                                  'cur_category': [],
                                                                  'categories': categories,
                                                                  'units': units,
                                                                  })


@admin_router.get('/unit/add')
def unit_add_page_view(request: Request):
    """Сторінка додавання одиниць вимірювання"""
    categories = get_categories()
    return templates.TemplateResponse(name='unit_add_form.html', context={'request': request,
                                                                          'cur_category': [],
                                                                          'categories': categories,
                                                                          })


@admin_router.post('/unit/add')
def unit_add_post(
        value: str = Form(),
):
    """POST-запит на додання одиниці вимірювання, передання інформації в БД"""
    unit_dto = UnitAddDTO.model_validate({'value': value})
    try:
        unit_add_orm(unit_dto)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/unit', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/unit/{pk}/delete')
def unit_delete(pk: int):
    """Видалення одиниці вимірювання з БД"""

    try:
        unit_delete_orm(pk)
    except UnmappedInstanceError as e:
        return {'detail': e}
    return RedirectResponse('/admin/unit', status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get('/unit/{pk}/')
def unit_update_form(request: Request, pk: int):
    """Форма редагування одиниці вимірювання"""
    categories = get_categories()
    unit = unit_get_by_id(pk)
    return templates.TemplateResponse(name='unit_update.html', context={'request': request,
                                                                        'cur_category': [],
                                                                        'categories': categories,
                                                                        'unit': unit,
                                                                        })


@admin_router.post('/unit/{pk}/')
def unit_update_post(pk: int, value: str = Form()):
    """POST-запит на редагування одиниці вимірювання"""
    try:
        unit_dto = UnitReadDTO.model_validate({
            'id': pk,
            'value': value,
        })
    except ValidationError as e:
        return {'detail': e.errors()}

    try:
        unit_update(unit_dto)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/unit', status_code=status.HTTP_303_SEE_OTHER)

from typing import Annotated, Optional

from fastapi import APIRouter, Body, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from exceptions import ExistORMObject
from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, UnitAddDTO, CategoryAddDTO, CounterAddDTO, \
    ProviderAddDTO, CurrencyDTO, AccountAddDTO
from utilities_accounting.db_api import get_category, get_rel_categories, get_providers_list, get_categories, \
    get_unit_list, \
    add_category_orm, add_category_and_counter, get_categories_counters, add_provider_orm, get_accounts_list, \
    get_currency_list, add_account_orm

router = APIRouter(prefix='/category', tags=['Main app'])
index_router = APIRouter(tags=['Index'])
admin_router = APIRouter(prefix='/admin', tags=['Admin'])
templates = Jinja2Templates(directory='templates')


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
    units = get_unit_list()
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
    # categories = get_categories()
    # units = get_unit_list()
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
    accounts = get_accounts_list()
    print(accounts)
    return templates.TemplateResponse(name='accounts.html', context={'request': request,
                                                                     'cur_category': [],
                                                                     'categories': categories,
                                                                     'accounts': accounts,
                                                                     })


@admin_router.get('/account/add')
async def page_add_account(request: Request):
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
    categories = get_categories()
    currencies = get_currency_list()
    return templates.TemplateResponse(name='currencies.html', context={'request': request,
                                                                        'cur_category': [],
                                                                        'categories': categories,
                                                                        'currencies': currencies,
                                                                        })


@admin_router.get('/currency/add')
def currency_add_page_view(request: Request):
    ...

@admin_router.post('/currency/add')
def currency_add_view():
    ...
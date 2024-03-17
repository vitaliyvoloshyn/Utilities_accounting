from typing import Annotated

from fastapi import APIRouter, Body, Form
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO, UnitAddDTO
from utilities_accounting.db_api import get_category, get_rel_categories, get_providers, get_categories, get_unit_list

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
def get_providers_list(request: Request):
    providers = get_providers()
    categories = get_categories()
    print(providers)
    return templates.TemplateResponse(name='providers.html', context={'request': request,
                                                                      'cur_category': [],
                                                                      'providers': providers,
                                                                      'categories': categories,
                                                                      })


@admin_router.get('/category')
async def get_category_list(request: Request):
    categories = get_categories()
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
async def add_category_post(request: Request, data: Annotated[str, int]):
    print(f"ggg {data}")
    categories = get_categories()
    units = get_unit_list()
    return templates.TemplateResponse(name='add_category.html', context={'request': request,
                                                                         'cur_category': [],
                                                                         'categories': categories,
                                                                         'units': units
                                                                         })

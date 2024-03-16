from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from utilities_accounting.schemas import CategoryDTO, CategoryRelDTO
from utilities_accounting.db_api import get_category, remove_parent, get_rel_categories, get_providers, get_categories

router = APIRouter(prefix='/category', tags=['Main app'])
index_router = APIRouter(tags=['Index'])
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


@index_router.get('/provider')
def get_providers_list(request: Request):
    providers = get_providers()
    categories = get_categories()
    print(providers)
    return templates.TemplateResponse(name='providers.html', context={'request': request,
                                                                      'cur_category': [],
                                                                      'providers': providers,
                                                                      'categories': categories,
                                                                      })


@router.delete('/parent/{pk}')
async def delete_parent(pk: int):
    return remove_parent(pk)

from typing import List

from fastapi import APIRouter, Form
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from utilities_accounting.db_api import get_categories
from utilities_accounting.repositories import counter_repository, category_repository, unit_repository

counter_router = APIRouter(prefix='/counter', tags=['Counter'])

templates = Jinja2Templates(directory='templates')

categories = category_repository.get_object_list()


@counter_router.get('/')
async def get_counter_list(request: Request):
    """Сторінка зі списком лічильників"""
    counters = counter_repository.get_object_list(with_relation=True)
    return templates.TemplateResponse(name='counters_list.html',
                                      context={
                                          'request': request,
                                          'categories': categories,
                                          # 'cur_category': [],
                                          'counters': counters,
                                      })


@counter_router.get('/add')
async def add_counter_form(request: Request):
    """Сторінка додання лічильника"""
    print('jjjjjjjjjjjj')
    units = unit_repository.get_object_list()
    return templates.TemplateResponse(name='counters_add_form.html',
                                      context={
                                          'request': request,
                                          'categories': categories,
                                          'cur_category': [],
                                          'units': units,
                                      })


@counter_router.get('/{pk}')
async def get_counter(request: Request, pk: int):
    """Сторінка з формою для редагування лічильника"""
    counter = counter_repository.get_object_by_id(pk, with_relation=True)
    units = unit_repository.get_object_list()
    return templates.TemplateResponse(name='counters_update_form.html',
                                      context={
                                          'request': request,
                                          'categories': categories,
                                          'units': units,
                                          'counter': counter,
                                      })




@counter_router.post('/add')
async def add_counter(
        name: str = Form(),
        unit_id: int = Form(),
        category_id: List[int] = Form()
):
    """POST-запит на додання лічильника, передання інформації в БД"""
    try:
        counter_repository.add({
            'unit_id': unit_id,
            'category_id': category_id,
            'name': name,
        })
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/counter', status_code=status.HTTP_303_SEE_OTHER)


@counter_router.post('/{pk}')
def update_counter(
        pk: int,
        name: str = Form(),
        unit_id: int = Form(),
        category_id: List[int] = Form()
):
    """POST-запит на редагування лічильника, передання інформації в БД"""
    try:
        counter_repository.update({
            'counter_id': pk,
            'unit_id': unit_id,
            'category_id': category_id,
            'name': name,
        })
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/counter', status_code=status.HTTP_303_SEE_OTHER)


@counter_router.get('/{pk}/delete')
def delete_counter(pk: int):
    """Видалення лічильника"""
    try:
        counter_repository.delete_object(pk)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/counter', status_code=status.HTTP_303_SEE_OTHER)

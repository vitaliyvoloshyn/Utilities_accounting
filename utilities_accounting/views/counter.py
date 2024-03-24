from fastapi import APIRouter, Form
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from utilities_accounting.db_api import get_categories
from utilities_accounting.models import Counter, Unit, Provider, Category
from utilities_accounting.repositories import BaseRepository
from utilities_accounting.schemas import CounterDTO, CounterAddDTO, UnitReadDTO, ProviderDTO, CategoryDTO, \
    CounterCategoryDTO

counter_router = APIRouter(prefix='/counter', tags=['Counter'])
counter_repo = BaseRepository(
    model=Counter,
    dto_read_model=CounterDTO
)
templates = Jinja2Templates(directory='templates')

categories = get_categories()


@counter_router.get('/')
async def get_counter_list(request: Request):
    """Сторінка зі списком лічильників"""
    counters = counter_repo.get_list_objects(model=Category, model_dto=CounterCategoryDTO)
    return templates.TemplateResponse(name='counters_list.html',
                                      context={
                                          'request': request,
                                          'categories': categories,
                                          'cur_category': [],
                                          'counters': counters,
                                      })


@counter_router.get('/add')
async def add_counter_form(request: Request):
    """Сторінка додання лічильника"""
    units = counter_repo.get_list_objects_another_model(Unit, UnitReadDTO)
    return templates.TemplateResponse(name='counters_add_form.html',
                                      context={
                                          'request': request,
                                          'categories': categories,
                                          'cur_category': [],
                                          'units': units,
                                      })


@counter_router.post('/add')
def unit_add_post(
        name: str = Form(),
        unit_id: int = Form(),
        category_id: int = Form()
):
    """POST-запит на додання лічильника, передання інформації в БД"""
    counter_dto = CounterAddDTO.model_validate({'name': name, 'unit_id': unit_id})
    try:
        counter_repo.add_counter(counter_dto, category_id)
    except IntegrityError as e:
        return {'detail': e}
    return RedirectResponse('/admin/counter', status_code=status.HTTP_303_SEE_OTHER)

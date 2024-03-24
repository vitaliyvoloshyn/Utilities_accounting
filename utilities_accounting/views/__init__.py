from fastapi import APIRouter
from .counter import counter_router

router_admin = APIRouter(prefix='/admin', tags=['Admin_v2'])

router_admin.include_router(counter_router)

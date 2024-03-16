import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import get_db
from utilities_accounting.views import router as utilities_router, index_router

app = FastAPI()
app.include_router(utilities_router)
app.include_router(index_router)
# app.include_router(water_router)
# app.include_router(main_router)
app.mount("/static/css", StaticFiles(directory="static/css"), name='css')
app.mount("/static/images", StaticFiles(directory="static/images"), name='images')
app.mount("/static/js", StaticFiles(directory="static/js"), name='js')

db = get_db()

if __name__ == "__main__":
    db.drop_db()
    db.create_db()
    db.insert_test_data()
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

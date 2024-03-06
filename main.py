import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import get_db

app = FastAPI()
# app.include_router(electricity_router)
# app.include_router(water_router)
# app.include_router(main_router)
app.mount("/static/css", StaticFiles(directory="static/css"))
app.mount("/static/images", StaticFiles(directory="static/images"))
app.mount("/static/js", StaticFiles(directory="static/js"))

db = get_db()

if __name__ == "__main__":
    db.drop_db()
    db.create_db()
    # db.insert_test_data()
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

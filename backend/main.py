from fastapi import FastAPI
from backend.database import create_db_and_tables
from backend.routes import todo

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(todo.router)

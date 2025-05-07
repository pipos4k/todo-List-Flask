from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Data(BaseModel):
    title: str
    description: str | None = None
    completed: bool

data_list = []

@app.post("/data")
def create_data(data: Data):

    data_list.append(data)

    return {
        "message": "Your data is received",
        "data": data
    }

@app.get("/data")
def bring_data():
    return data_list
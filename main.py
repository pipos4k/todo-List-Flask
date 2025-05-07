from fastapi import FastAPI
from pydantic import BaseModel
import datetime
app = FastAPI()
count =1 
data_list = []

class Data(BaseModel):
    title: str
    description: str | None = None
    completed: bool

@app.post("/data")
def create_data(data: Data):
    global count

    new_data = data.dict()
    new_data["id"] = count
    new_data["date"] = datetime.datetime.utcnow().isoformat()

    data_list.append(new_data)
    count +=1

    return {
        "message": "Your data is received",
        "data": new_data
    }

@app.get("/data")
def bring_data():
    return data_list


@app.get("/data/{id}")
def brind_id_data(id: int):
    for data in data_list:
        if data["id"] == id:
            return data
    return {"error": "Data not found"}

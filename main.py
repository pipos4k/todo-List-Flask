from fastapi import FastAPI # Local host
from pydantic import BaseModel # Creates a json format data
from sqlmodel import SQLModel, create_engine, Field, Session # for Database
import datetime # Save data's time
from typing import Optional

app = FastAPI()
count =1 # For Data's ID
data_list = [] # To save our data for /data

# Setup our SQLite database
sqlite_data = "database.db"
sqlite_url = f"sqlite:///{sqlite_data}"
engine = create_engine(sqlite_url, echo=True) # The engine is what connects SQLModel to the database

# new class for real table Data
class Data_SQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    complted: bool = False

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# class, format data
class Data(BaseModel):
    title: str
    description: str | None = None
    completed: bool

# Post data to /data
@app.post("/data")
def create_data(data: Data):
    global count

    new_data = data.model_dump() # use class Data format/save it to new_data
    new_data["id"] = count
    new_data["date"] = datetime.datetime.now(datetime.timezone.utc)().isoformat()

    data_list.append(new_data) 
    count +=1

    return {
        "message": "Your data is received",
        "data": new_data
    }

# Get data
@app.get("/data")
def bring_data():
    return data_list


# Get data by id
@app.get("/data/{id}")
def brind_id_data(id: int):
    for data in data_list:
        if data["id"] == id:
            return data
    return {"error": "Data not found"}

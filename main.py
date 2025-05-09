from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field, Session, select
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Setup DB
sqlite_file = "todo.db"
sqlite_url = f"sqlite:///{sqlite_file}"
engine = create_engine(sqlite_url, echo=True)

# DB Model
class Data_SQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False

# Model for input (no ID)
class DataCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Model for update (with optional fields)
class DataUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Create the database table
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Get all data from /data
@app.get("/data")
def get_data():
    with Session(engine) as session:
        statement = select(Data_SQL)
        results = session.exec(statement).all()
        return results

# Post data to /data
@app.post("/data")
def create_data(data: DataCreate):
    new_data = Data_SQL.from_orm(data)
    with Session(engine) as session:
        session.add(new_data)
        session.commit()
        session.refresh(new_data)
        return new_data

# Update data by id
@app.post("/data/{id}")
def update_data(id: int, updated_data: DataCreate):
    with Session(engine) as session:
        data_item = session.get(Data_SQL, id)
        if not data_item:
            return "Data not found"
        
        data_item.title = updated_data.title
        data_item.description = updated_data.description
        data_item.completed = updated_data.completed

        session.add(data_item)
        session.commit()
        session.refresh(data_item)
        return data_item
    
# Delete a data by id
@app.delete("/data/{id}")
def delete_data(id: int):
    with Session(engine) as session:
        data = session.get(Data_SQL, id)
        if not data:
            return "Data not found"
        
        session.delete(data)
        session.commit()
        return data

# Update data by id (specific field)
@app.patch("/data/{id}")
def patch_data(id: int, data_patch: DataUpdate):
    with Session(engine) as session:
        data = session.get(Data_SQL, id)

        update_data = data_patch.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(data, key, value)

        session.add(data)
        session.commit()
        session.refresh(data)
        return data


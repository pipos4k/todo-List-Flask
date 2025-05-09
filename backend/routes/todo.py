from fastapi import APIRouter, Query
from sqlmodel import Session, select
from backend.models.todo import Data_SQL, DataCreate, DataUpdate
from backend.database import engine
from sqlalchemy import asc, desc
from typing import List, Optional

router = APIRouter()

# Get all data from /data, And search for specific title/complete(true/false)
@router.get("/data", response_model=List[Data_SQL])
def get_data(title: Optional[str] = Query(None), 
            completed: Optional[bool] = Query(None),
            limit: int = Query(10, ge=1),
            offset: int = Query(0, ge=0),
            sort_by: str = Query("id", pattern="^(id|title|completed)$"),
            sort_order: str = Query("asc", pattern="^(asc|desc)$")
            ):
    
    with Session(engine) as session:
        statement = select(Data_SQL)

        if title is not None:
            statement = statement.where(Data_SQL.title.contains(title))
        if completed is not None:
            statement = statement.where(Data_SQL.completed == completed)
        
        # Sorting
        sort_column = getattr(Data_SQL, sort_by)
        if sort_order == "asc":
            statement = statement.order_by(asc(sort_column))
        else:
            statement = statement.order_by(desc(sort_column))

        # Pagination
        statement = statement.offset(offset).limit(limit)
        results = session.exec(statement).all()
        return results

# Post data
@router.post("/data")
def create_data(data: DataCreate):
    new_data = Data_SQL.from_orm(data)
    with Session(engine) as session:
        session.add(new_data)
        session.commit()
        session.refresh(new_data)
        return new_data

# Allow both PATCH and PUT (ammend a data)
@router.patch("/data/{id}")
@router.put("/data/{id}")  
def update_data(id: int, data_update: DataUpdate):
    with Session(engine) as session:
        data_item = session.get(Data_SQL, id)
        if not data_item:
            return "Error, Data not found"
        
        updates = data_update.dict(exclude_unset=True)
        for key, value in updates.items():
            setattr(data_item, key, value)

        session.add(data_item)
        session.commit()
        session.refresh(data_item)
        return data_item
    
# Delete a data by id
@router.delete("/data/{id}")
def delete_data(id: int):
    with Session(engine) as session:
        data = session.get(Data_SQL, id)
        if not data:
            return "Data not found"
        
        session.delete(data)
        session.commit()
        return data
    
@router.delete("/data")
def delete_all_data():
    with Session(engine) as session:
        statement = select(Data_SQL)
        results = session.exec(statement).all()
    
        for item in results:
            session.delete(item)
        session.commit()

        return {"message": f"Deleted {len(results)} items."}

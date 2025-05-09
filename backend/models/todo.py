from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

# DB Model to add unique ID
class Data_SQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False

# DB Model for input (no ID)
class DataCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# DB Model for update (with optional fields)
class DataUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
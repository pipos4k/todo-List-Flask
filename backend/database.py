from sqlmodel import create_engine, SQLModel

# Setup DB
sqlite_file = "todo.db"
sqlite_url = f"sqlite:///{sqlite_file}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
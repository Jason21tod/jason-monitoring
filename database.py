import uuid
import os
from sqlmodel import Field, Session, SQLModel, create_engine, select

DB_URL = str(os.environ.get("TEST_DB_STAR"))

class KidsTable(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    name: str


engine = create_engine(DB_URL, echo=True)
SQLModel.metadata.create_all(engine)
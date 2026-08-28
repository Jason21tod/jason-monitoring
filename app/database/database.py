import uuid
import logging
import os
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select


logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

database_logger = logging.getLogger("james_bond (database watcher)")

DB_URL = str(os.environ.get("DATABASE_URL"))

class KidsTable(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    name: str
    age: int = Field(default= 3)
    parent: str
    room: int
    checkin: datetime
    checkout: datetime
    notations: str
    can_swin: bool
    can_pay: bool = Field(default= True)


engine = create_engine(DB_URL, echo=True)
try:
    SQLModel.metadata.create_all(engine)
except:
    database_logger.warning("Error on creating tables")


def get_kids(session: Session):
    statement = select(KidsTable)
    return session.exec(statement)

def get_kids_by_age(session: Session, min_age: int, max_age):
    stmt = select(KidsTable).where(KidsTable.age.between(min_age, max_age))
    return session.exec(stmt)


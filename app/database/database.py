import uuid
import logging
import os
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from app.email import report_error_by_email


logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

database_logger = logging.getLogger("james_bond (database watcher)")

DB_URL = str(os.environ.get("DATABASE_URL"))

engine = create_engine(DB_URL, echo=True)

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


try:
    SQLModel.metadata.create_all(engine)
except:
    report_error_by_email("Error on creating tables", "A error on creating tables has been ocurred, verify the Database availability")
    database_logger.warning("Error on creating tables")


def get_kids(session: Session):
    statement = select(KidsTable)
    return session.exec(statement)

def get_kids_by_age(session: Session, min_age: int, max_age):
    statement = select(KidsTable).where(KidsTable.age.between(min_age, max_age))
    return session.exec(statement)

def delete_kid_by_id(id):
    with Session(engine) as session:
        kid = session.get(KidsTable, id)
        if kid: 
            session.delete(kid)
            session.commit()
            print(f"Register of ID {id} excluded.")
        else:
            print(f"This ID does not exist{id}.")
def add_new_kid(kid: KidsTable):
    with Session(engine) as session:
        session.add(kid)
        session.commit()

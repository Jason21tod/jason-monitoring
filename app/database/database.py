import uuid
import logging
import os
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine


logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

database_logger = logging.getLogger("james_bond (database watcher)")

DB_URL = str(os.environ.get("jason_monitoring_sb_url"))

class KidsTable(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    name: str
    checkin: datetime
    checkout: datetime
    notations: str
    can_swin: bool
    can_pay: bool


engine = create_engine(DB_URL, echo=True)
try:
    SQLModel.metadata.create_all(engine)
except:
    database_logger.warning("Error on creating tables")
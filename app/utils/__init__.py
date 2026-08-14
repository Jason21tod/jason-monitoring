import datetime

from starlette.datastructures import FormData
from uuid import uuid4

from ..database.database import KidsTable



def make_a_kids_table_object(form: FormData):
    def format_room_type(form):
        try:
            return int(form.get("room"))
        except:
            raise TypeError("Room type its not a integer or integer convertable")
    try:
        uuid = uuid4()
        formated_room_type = format_room_type(form)
        kid = KidsTable(
            id = uuid,
            name= str(form.get("name")),
            age= int(form.get("age")),
            parent = str(form.get("parent")),
            room = formated_room_type,
            checkin= form.get("checkin"),
            checkout= form.get("checkout"),
            can_pay= bool(form.get("can_pay")),
            can_swin= bool(form.get("can_swin")),
            notations= str(form.get("notations"))
        )
        return kid
    except:
        raise TypeError("The object its not a valid format")

def make_mock_kids_table_object():
    uuid = uuid4()
    kid = KidsTable(
        id=uuid,
        name="test",
        age= 8,
        parent = "test parent",
        room = 1,
        checkin=datetime.datetime.now(),
        checkout= datetime.datetime.now(),
        can_pay=True,
        can_swin=True,
        notations=""
    )
    return kid
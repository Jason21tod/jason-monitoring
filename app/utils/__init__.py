import datetime
from datetime import datetime
from fastapi.responses import Response

from uuid import uuid4

from ..database.database import KidsTable



def make_a_kids_table_object(data):
    try:
        uuid = uuid4()
        formated_room_type = format_room_type(data)
        formated_checkin = format_date_type(data.get("checkin"))
        formated_checkout = format_date_type(data.get("checkout"))
        if is_checkin_early_than_checkout(formated_checkin, formated_checkout):
            kid = KidsTable(
                id = uuid,
                name= str(data.get("name")),
                age= int(data.get("age")),
                parent = str(data.get("parent")),
                room = formated_room_type,
                checkin= formated_checkin,
                checkout= formated_checkout,
                can_pay= bool(data.get("can_pay")),
                can_swin= bool(data.get("can_swin")),
                notations= str(data.get("notations"))
            )
            return kid
        else:
            print(f"ERROR - The checkin and checkout are not cohese - {formated_checkin} X {formated_checkout}")
            return Response(f"The checkin and checkout are not cohese - {formated_checkin} X {formated_checkout}", 404)
    except:
        print(f" ERROR - The object its not a valid format")
        return Response(f"The object its not a valid format")

def format_room_type(form):
    try:
        return int(form.get("room"))
    except:
        raise TypeError("Room type its not a integer or integer convertable")

def is_checkin_early_than_checkout(checkin: datetime, checkout: datetime):
    if checkout > checkin:
        print("all date's okay")
        return True
    return False

def format_date_type(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except:
        raise TypeError(f"One of the dates could not be converted to Datetime objects - {date_str}")

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
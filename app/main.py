import datetime
import logging

from fastapi import FastAPI, Request, logger, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from uuid import uuid4

from .api.api import MsgObject, MsgData
from .whatsapp.whatsapp_sys import send_test_message, send_message
from .whatsapp.msg_handlers import ComplimentHandler
from .api.api_authentication import AuthenticationVerifier
from .database.database import engine, KidsTable


app = FastAPI(title="Jason Monitoring System")

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
main_logger = logging.getLogger("Maid (Main Logger)")


@app.get("/")
def home():
    return {"hello":"world!"}

@app.post("/add_kids")
async def add_kids_to_db(request: Request):
    main_logger.info("Added new kid...")
    uuid = uuid4()
    form = await request.form()
    kid = KidsTable(
        id = uuid,
        name= form.get("name"),
        checkin= form.get("checkin"),
        checkout= form.get("checkout"),
        can_pay= bool(form.get("can_pay")),
        can_swin= bool(form.get("can_swin")),
        notations= str(form.get("notations"))
    )

    with Session(engine) as session:
        session.add(kid)
        session.commit()

    # Change the way that url are made after that prototype
    main_logger.info("Added New Kid!")
    return RedirectResponse(url="https://www.jasonuniverse.com.br/jason-monitoring-demo.html", status_code= 201)

@app.get("/add_test")
def add():
    uuid = uuid4()

    kid = KidsTable(
            id=uuid,
            name="test",
            checkin=datetime.datetime.now(),
            checkout= datetime.datetime.now(),
            can_pay=True,
            can_swin=True,
            notations=""
        )
    
    with Session(engine) as session:
        session.add(kid)
        session.commit()

    return 200

@app.post("/msg")
async def msg(request: Request, _:None = Depends(AuthenticationVerifier.verify_account_sid)):
    try:
        data = await request.form()
    except:
        main_logger.warning("ERROR ON RECEIVENG MSG REQUEST ON MSG ENDPOINT - the request isn't a valid message")
        return 400
    response_msg_object = create_response(data)
    main_logger.debug("message responsed!")
    return send_message(msg_object=response_msg_object)

def create_response(data):
    first_receiver = ComplimentHandler()
    received_message = MsgData(
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(data.get("Body")),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )
    new_received_msg = MsgObject(received_message)

    message_body = first_receiver.receive_message(new_received_msg)
    response_msg_data = MsgData (
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(message_body),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )
    
    return MsgObject(response_msg_data)

@app.post("/test_msg")
async def test_msg(request: Request):
    data = await request.form()

    customer_number = str(data.get("From"))
    name = data.get("ProfileName")

    if (type(name)) == str:
        send_test_message(name, customer_number)
        return {"status": 200}
    
    return {"status": 400}
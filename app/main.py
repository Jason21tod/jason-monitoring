import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from starlette.datastructures import FormData


from .api.msg_objects import MsgObject, MsgData
from .whatsapp.whatsapp_sys import send_test_message, send_message
from .whatsapp.msg_handlers import ComplimentGetter
from .api.api_authentication import TwilioAuthenticator, DatabaseGateKeeper
from .database.database import engine
from .utils import make_a_kids_table_object, make_mock_kids_table_object

app = FastAPI(title="Jason Monitoring System")

origins = [
    "http://127.0.0.1:5500",
    "https://jason-portfolio-frontend.vercel.app/",
    "https://www.jasonuniverse.com.br"
]

app.add_middleware(
    CORSMiddleware,
        allow_origins=origins, # Specific origins
        allow_credentials=True, # Allow cookies/auth headers
        allow_methods=["*"], # Allow all HTTP methods
        allow_headers=["*"], # Allow all headers
)

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
main_logger = logging.getLogger("Maid (Main Logger)")



@app.get("/")
def home():
    return {"hello":"world!"}

@app.get("/get_kids")
async def get_kids(
        _: None = Depends(DatabaseGateKeeper.verify_secret)
    ):
    
    return {"status": "Done"}

@app.post("/add_kids")
async def add_kids_to_db(request: Request):
    main_logger.info("Added new kid...")
    form = await request.json()
    print(form)
    kid = make_a_kids_table_object(form)

    with Session(engine) as session:
        session.add(kid)
        session.commit()

    # Change the way that url are made after that prototype
    main_logger.info("Added New Kid!")
    return RedirectResponse(url="https://www.jasonuniverse.com.br/jason-monitoring-demo.html", status_code= 303)

@app.get("/add_test")
def add():
    with Session(engine) as session:
        kid = make_mock_kids_table_object()
        session.add(kid)
        session.commit()

    return 200

@app.post("/msg")
async def msg(request: Request, _:None = Depends(TwilioAuthenticator.verify_credentials)):
    main_logger.info("new message received")
    try:
        data = await request.form()
    except:
        main_logger.warning("ERROR ON RECEIVENG MSG REQUEST ON MSG ENDPOINT - the request isn't a valid message")
        return 400
    response_msg_object = create_response(data)
    main_logger.info("message responsed!")
    return send_message(msg_object=response_msg_object)

def create_response(data: FormData):
    received_message = make_msg_data(data)
    response_msg_data = make_response_msg_by_received_msg(data, received_message)
    return MsgObject(response_msg_data)

def make_msg_data(data: FormData):
    return MsgData(
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(data.get("Body")),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )

def make_response_msg_by_received_msg(data: FormData, received_message: MsgData):
    first_receiver = ComplimentGetter()
    new_received_msg = MsgObject(received_message)
    message_body = first_receiver.respond_message(new_received_msg)
    return MsgData (
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(message_body),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )

@app.post("/test_msg")
async def test_msg(request: Request):
    data = await request.form()

    customer_number = str(data.get("From"))
    name = data.get("ProfileName")

    if (type(name)) == str:
        send_test_message(name, customer_number)
        return {"status": 200}
    
    return {"status": 400}
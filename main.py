from fastapi import FastAPI, Request, logger
from api import MsgObject, MsgData
from whatsapp_sys import send_test_message, send_message
from msg_handlers import ComplimentHandler


app = FastAPI(title="Jason Monitoring System")


@app.get("/")
def home():
    return {"hello":"world!"}


@app.post("/msg")
async def msg(request: Request):
    try:
        data = await request.form()
    except:
        logger.logger.warning("ERROR ON RECEIVENG MSG REQUEST ON MSG ENDPOINT - the request isn't a valid message")
        return 400
    response_msg_object = create_response(data)
    return send_message(msg_object=response_msg_object)

def create_response(data):
    receiver = ComplimentHandler()
    received_message = MsgData(
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(data.get("Body")),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )
    new_received_msg = MsgObject(received_message)

    message_body = receiver.receive_message(new_received_msg)
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
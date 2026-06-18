from fastapi import FastAPI, Request, logger
from api import MsgObject, MsgData
from whatsapp_sys import send_test_message, send_message
from msg_handlers import FirstReceiver


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
    received_data = MsgData(
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(data.get("Body")),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )
    new_msg_object = MsgObject(received_data)
    receiver = FirstReceiver()
    message_body = receiver.receive_message(new_msg_object)
    sent_data = MsgData (
            str(data.get("ProfileName")),
            str(data.get("To")),
            str(message_body),
            str(data.get("From")),
            str(data.get("SmsStatus"))
        )
    response_msg_object = MsgObject(sent_data)
    print(response_msg_object.body)
    return send_message(msg_object=response_msg_object)



@app.post("/test_msg")
async def test_msg(request: Request):
    data = await request.form()

    customer_number = str(data.get("From"))
    name = data.get("ProfileName")

    if (type(name)) == str:
        send_test_message(name, customer_number)
        return {"status": 200}
    
    return {"status": 400}
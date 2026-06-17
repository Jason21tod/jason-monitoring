from fastapi import FastAPI, Request, logger
from starlette.datastructures import FormData
from whatsapp_sys import send_test_message


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
    new_msg_object = MsgObject(data)


class MsgObject:
    def __init__(self, data: FormData) -> None:
        self.name = data.get("ProfileName")
        self.to = data.get("To")
        self.body = data.get("Body")
        self._from = data.get("From")
        self.status = data.get("SmsStatus")

        print(f"Name: {self.name}")
        print(f"To: {self.to}")
        print(f"body: {self.body}")
        print(f"from: {self._from}")
        print(f"status: {self.status}")


    


@app.post("/test_msg")
async def test_msg(request: Request):
    data = await request.form()

    customer_number = str(data.get("From"))
    name = data.get("ProfileName")

    if (type(name)) == str:
        send_test_message(name, customer_number)
        return {"status": 200}
    
    return {"status": 400}
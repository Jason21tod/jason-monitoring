from fastapi import FastAPI, Request
from whatsapp_sys import send_test_message


app = FastAPI()


@app.get("/")
def home():
    return {"hello":"world!"}


@app.post("/test_msg")
async def msg_post(request: Request):
    data = await request.form()

    customer_number = str(data.get("From"))
    name = data.get("ProfileName")

    if (type(name)) == str:
        send_test_message(name, customer_number)
        return {"status": 200}
    
    return {"status": 400}
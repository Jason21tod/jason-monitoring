from fastapi import FastAPI, Request
from whatsapp_sys import send_test_message


app = FastAPI()


@app.get("/")
def home():
    return {"hello":"world!"}



@app.post("/test_msg")
async def msg_post(request: Request):
    data = await request.form()
    name = data.get("ProfileName")
    if (type(name)) ==  str:
        send_test_message(name)
        return {"status": 200}
    return {"status": 400}
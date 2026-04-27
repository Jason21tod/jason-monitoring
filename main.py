from fastapi import FastAPI
from twilio.rest import Client
from pydantic import BaseModel
import os


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SSID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TESTER_CELLPHONE_NUMBER = os.environ.get("TESTER_CELPHONE_NUMBER")


twilio_client: Client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = FastAPI()


class Item(BaseModel):
    pass

@app.get("/")
def home():
    return {"hello":"world!"}


@app.post("/msg")
def msg_post():
    if TESTER_CELLPHONE_NUMBER != None:
        message = twilio_client.messages.create(
                from_='whatsapp:+14155238886',
                body= "Bem vindo ao teste testado testando nos testes",
                to=TESTER_CELLPHONE_NUMBER
            )
        return {"status": 200}
    return {"status": 400}
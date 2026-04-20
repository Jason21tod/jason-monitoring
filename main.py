from fastapi import FastAPI
from twilio.rest import Client
import os


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SSID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


twilio_client: Client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = FastAPI()


@app.get("/")
def home():
    return {"hello":"world!"}
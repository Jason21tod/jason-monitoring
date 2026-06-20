from twilio.rest import Client
from api import MsgObject
import os


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TESTER_CELLPHONE_NUMBER = os.environ.get("TESTER_CELLPHONE_NUMBER")

if TWILIO_ACCOUNT_SID == None or TWILIO_AUTH_TOKEN == None or TESTER_CELLPHONE_NUMBER == None:
    raise Exception("Error, some of your Twilio env var are None, fix and try again")

twilio_client: Client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_test_message(name: str, customer_number: str):
    if customer_number != "None":
        message = twilio_client.messages.create(
                from_='whatsapp:+14155238886',
                body= f"Bem vindo(a) {name} ao teste testado testando nos testes",
                to= customer_number
            )
        return "200"
    print("ERROR -> COULD NOT SEND MESSAGE! THE TARGET IS NONE")
    return "400"

def send_message(msg_object: MsgObject):
    if msg_object._from != "None":
        message = twilio_client.messages.create(
                from_=msg_object.to,
                body= msg_object.body,
                to= msg_object._from
            )
        print(message.status)
        return "200"
    print("ERROR -> COULD NOT SEND MESSAGE! THE TARGET IS NONE")
    return "400"

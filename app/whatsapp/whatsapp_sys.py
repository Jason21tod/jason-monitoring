from twilio.rest import Client
from app.api.msg_objects import MsgObject
import os
import logging

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TESTER_CELLPHONE_NUMBER = os.environ.get("TESTER_CELLPHONE_NUMBER")



logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
whatsapp_logger = logging.getLogger("Cleyton (Whatsapp Watcher)")

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
    whatsapp_logger.warning("ERROR -> COULD NOT SEND MESSAGE! THE TARGET IS NONE")
    return "400"

def send_message(msg_object: MsgObject):
    print(msg_object.body)
    line = 0
    char_count = 0
    for char in msg_object.body:
        char_count += 1
        if char == "\n":
            line += 1
            if char_count >= 1500:
                twilio_client.messages.create(
                                from_=msg_object.to,
                                body= msg_object.body[0:char_count],
                                to= msg_object._from
                            )
                twilio_client.messages.create(
                                from_=msg_object.to,
                                body= msg_object.body[char_count:],
                                to= msg_object._from
                            )
                return 200
                         
    if msg_object._from != "None":
        message = twilio_client.messages.create(
                from_=msg_object.to,
                body= msg_object.body,
                to= msg_object._from
            )
        whatsapp_logger.info(message.status)
        return 200
    whatsapp_logger.warning("ERROR -> COULD NOT SEND MESSAGE! THE TARGET IS NONE")
    return 400

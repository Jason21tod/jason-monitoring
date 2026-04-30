from twilio.rest import Client
from abc import ABC, abstractmethod
import os


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TESTER_CELLPHONE_NUMBER = os.environ.get("TESTER_CELLPHONE_NUMBER")

if TWILIO_ACCOUNT_SID == None or TWILIO_AUTH_TOKEN == None or TESTER_CELLPHONE_NUMBER == None:
    raise Exception("Error, some of your Twilio env var are None, fix and try again")

twilio_client: Client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class MessageReceiver(ABC):
    @abstractmethod
    def receive_message(self):
        pass


def send_test_message(name: str):
    if TESTER_CELLPHONE_NUMBER != None:
        message = twilio_client.messages.create(
                from_='whatsapp:+14155238886',
                body= f"Bem vindo(a) {name} ao teste testado testando nos testes",
                to=TESTER_CELLPHONE_NUMBER
            )
    print("ERROR -> COULD NOT SEND MESSAGE! THE TARGET IS NONE")
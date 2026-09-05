from twilio.rest import Client
from app.api.msg_objects import MsgObject
import os
import logging

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TESTER_CELLPHONE_NUMBER = os.environ.get("TESTER_CELLPHONE_NUMBER")



class MessageSender:
    def __init__(self, msg_object: MsgObject) -> None:
        self.msg_object: MsgObject = msg_object    

    def is_necessary_multiple_responses(self, current_char: str, char_count: int):
        if current_char == "\n":
            if self.is_in_char_limit(char_count):
                return True
        return False

    def is_in_char_limit(self, char_count: int):
        if char_count >= 1500:
            return True
        return False

    def send_char_limit_messages(self, char_count:int):
        first_body =  self.msg_object.body[0:char_count]
        self.create_response(first_body)

        second_body = self.msg_object.body[char_count:]
        self.create_response(second_body)

    def create_response(self, body):
        print(f"response -> {body}")
        print(twilio_client.messages.create(
                    from_=self.msg_object.to,
                    body= body,
                    to= self.msg_object._from
                ).status)

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
    if msg_object._from != "None":
        return send_messages(msg_object)
    whatsapp_logger.warning("ERROR -> COULD NOT SEND MESSAGE! THE TARGET IS NONE")
    return 400

def send_messages(msg_object: MsgObject):
    message_sender = MessageSender(msg_object)
    verify_multiple_messages(message_sender)
    message_sender.create_response(msg_object.body)
    return 200

def verify_multiple_messages(message_sender: MessageSender):
    char_count = 0
    for current_char in message_sender.msg_object.body:
        char_count += 1
        if message_sender.is_necessary_multiple_responses(current_char, char_count):
            message_sender.send_char_limit_messages(char_count)
            return True
    else:
        return False

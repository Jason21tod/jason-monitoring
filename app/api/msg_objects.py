from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class MsgData:
    name: str
    to: str
    body: str
    _from: str
    status: str

class MsgObject:
    def __init__(self, data: MsgData) -> None:
        self.name: str = data.name
        self.to: str = data.to
        self.body: str = data.body
        self._from: str = data._from
        self.status: str = data.status


class MsgHandler(ABC):
    msg_handlers: list = []
    _msg = "This is a Placeholder msg - should be configured"
    _handler_name = "Abstract Handler name - should be configured"
    _help_message = "This is a Help message and should be configured"
    _not_processed_msg = "Então... Não entendi oque quiz dizer, perdão! digite help para ter uma ideia doque posso fazer."
    _brief_desc = "Uma descrição breve..."


    @abstractmethod
    def respond_message(self, msg: MsgObject):
        """This method should be the entrypoint of the class"""        
        pass


    @abstractmethod
    def verify_gatling(self, body: str):
        """This method should be used to implement the gatling to trigger the message"""
        pass

    def set_msg(self, msg:str):
        """This method only could be chaged if you need a special way to set message"""
        self._msg = msg

    @abstractmethod
    def format_msg(self):
        pass

    @abstractmethod
    def pass_to_next(self, msg: MsgObject):
        pass

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
    _handler_name = "Abstract Handler name"
    _help_message = "This is a Help message and should be configured"
    _not_processed_msg = "Então... Não entendi oque quiz dizer, perdão!"
    _brief_desc = "Uma descrição breve..."

    @abstractmethod
    def verify_gatling(self, body: str):
        pass

    def set_msg(self, msg:str):
        self._msg = msg

    @abstractmethod
    def respond_message(self, msg: MsgObject):
        pass

    @abstractmethod
    def format_msg(self):
        pass

    @abstractmethod
    def pass_to_next(self, msg: MsgObject):
        pass

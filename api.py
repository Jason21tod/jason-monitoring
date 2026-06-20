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

    msg_handlers: list
    _msg = "This is a Placeholder msg - should be configured"

    @abstractmethod
    def verify_gatling(self, body: str):
        pass

    def set_msg(self, msg:str):
        self._msg = msg

    @abstractmethod
    def receive_message(self, msg: MsgObject):
        pass
    
    @abstractmethod
    def pass_to_next(self, msg: MsgObject):
        if len(self.msg_handlers) == 0:
            print("Could not send a message -> Unknow command or content")
            return "Então... Não entendi oque quiz dizer, perdão!"
        else:
            for handler in self.msg_handlers:
                return handler.receive_message(msg)

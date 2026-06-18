from api import MsgHandler, MsgObject

class FirstReceiver(MsgHandler):
    msg_handlers: list[MsgHandler]= []
    __compliment_list = ["oi", "olá", "hello"]
    _msg = ""

    def receive_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("hit the greetings message... processing")
            self.set_msg(f"Olá {msg.name}!")
            return self._msg
        else:
            return self.pass_to_next(msg)

    def verify_gatling(self, body: str):
        formated_body = self.formatBody(body)
        for compliment in self.__compliment_list:
            if compliment in formated_body:
                return True
            else:
                pass
        return False
    

    def formatBody(self, body: str):
        space_index = body.find(" ")
        if self.isShortMessage(space_index):
            return body 
        else:
            return body[0:space_index]
        

    def isShortMessage(self, space_index: int):
        if space_index == -1:
            return True
        return False

    def pass_to_next(self, msg: MsgObject):
        return super().pass_to_next(msg)
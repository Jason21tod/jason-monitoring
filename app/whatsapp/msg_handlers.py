from app.api.msg import MsgHandler, MsgObject
from app.database.database import Session, select, KidsTable, engine


class GetAllKidsVerifier(MsgHandler):
    def receive_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("Getting all the data from kids...")
            self.format_msg()
            return self._msg
        else:
            return self.pass_to_next(msg)

    def format_msg(self):
        with Session(engine) as session:
            statement = select(KidsTable)
            kids = session.exec(statement)
            
            msg = """Lista de todas as crianças \n\n"""
            
            for kid in kids:
                msg = msg + f"{kid.name} - {kid.room} - {kid.parent}\n"
            self.set_msg(msg)

    def verify_gatling(self, body: str):
        if body == "lista geral":
            return True
        return False

class ComplimentVerifier(MsgHandler):
    get_all_kids_verifier = GetAllKidsVerifier()
    msg_handlers: list= [get_all_kids_verifier]
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

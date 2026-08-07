from app.api.msg import MsgHandler, MsgObject
from app.database.database import Session, select, KidsTable, engine


    
def is_short_message(space_index: int):
    if space_index == -1:
        return True
    return False


class GetAllKidsVerifier(MsgHandler):
    _handler_name = "lista geral"
    _help_message = f"*{_handler_name}* -> Usado para obter a lista de todas as crianças. \n\n A ordem dos dados é: \n\n Nome da criança | Número do quarto | Pais/responsáveis"
    _brief_desc = "Exibe a lista de todos as crianças."

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
        if body == self._handler_name:
            return True
        return False

class HelpVerifier(MsgHandler):
    get_all_kids_verifier = GetAllKidsVerifier()
    msg_handlers: list[MsgHandler] = [get_all_kids_verifier]
    _handler_name = "help"
    _help_message = "Claro! eu lhe mostrarei os comandos! Dica extra: Você pode usar _help nome do comando_ para saber mais sobre ele\n\n"

    def receive_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("A help message received!")
            print(self.find_msg_after_help(msg.body.lower()))
            formated_msg = self.format_msg(msg.body.lower())
            if formated_msg == self._handler_name:
                print("...general help message")
                self.make_general_help_message()
                self.set_msg(self._help_message)
            else:
                print("...not general help message")
                for handler in self.msg_handlers:
                    if formated_msg == handler._handler_name:
                        print(f"{handler._handler_name}... help message")
                        self.set_msg(handler._help_message)
            return self._msg
        else:
            return self.pass_to_next(msg) 

    def verify_gatling(self, body):
        if self.first_word_is_help(body):
            return True
        return False

    def make_general_help_message(self):
        _help_message = "Claro! eu lhe mostrarei os comandos! Dica extra: Você pode usar help <Nome do comando> para saber mais sobre ele\n\n"
        for handler in self.msg_handlers:
            self._help_message += f"*{handler._handler_name}* -> {handler._brief_desc}"
    
    def first_word_is_help(self, body):
        space_index = body.find(" ")
        if space_index == -1 and body == self._handler_name:
            return True
        if body[0:space_index] == self._handler_name:
            return True
        return False

    def find_msg_after_help(self, body:str):
        space_index = body.find(" ")
        return body[space_index:].strip()

    def format_msg(self, body: str):
        space_index = body.find(" ")
        if is_short_message(space_index):
            return body
        return body[space_index+1:]

class ComplimentVerifier(MsgHandler):
    get_all_kids_verifier = GetAllKidsVerifier()
    help_verifier = HelpVerifier()
    msg_handlers: list= [help_verifier, get_all_kids_verifier]
    __compliment_list = ["oi", "olá", "hello"]
    _msg = ""

    def receive_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("hit the greetings message... processing")
            self.set_msg(f"Olá {msg.name}! Precisa de ajuda? Digite *Help* e eu lhe mostro oque sei fazer por enquanto!")
            return self._msg
        else:
            return self.pass_to_next(msg)

    def verify_gatling(self, body: str):
        formated_body = self.format_msg(body)
        for compliment in self.__compliment_list:
            if compliment in formated_body:
                return True
            else:
                pass
        return False

    def format_msg(self, body: str):
        space_index = body.find(" ")
        if is_short_message(space_index):
            return body
        return body[0:space_index]


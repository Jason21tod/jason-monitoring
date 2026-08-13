from app.api.msg_objects import MsgHandler, MsgObject
from app.database.database import Session, engine, get_kids
import re

"""The order of the classes here are inverted on pupose.
after made the primary classes, we gonna change the whole system to a new archive
and maybe split it
"""

DESCRIPTION_MESSAGE = """
Sou Jason, um assistênte de monitoria criado por Gian Pereira!

Você está falando com uma versão demo da minha aplicação, sou muito mais doque os olhos podem ver. \U0001F4BB
                
Fui criado com o propósito de ajudar equipes de recreação a ordenar, monitorar e listar crianças, bem como ajudar a localizar cada criança que requeira mais atenção.

Fui desenvolvido no período em que meu criador trabalhava no Clara Resorts. Caso queira saber mais sobre o trabalho dele, acesse:

https://www.jasonuniverse.com.br

Caso queira sabe oque eu faço, digite *"help"*.
"""


def is_short_message(space_index: int):
    if space_index == -1:
        return True
    return False


class GetWhoYouAre(MsgHandler):
    _handler_name = "quem é você?"
    _brief_desc = """Uma breve descrição de quem sou e quem me criou!"""
    gatlings = ["quem é você?", "quem e voce", "quem é vc?", "quem e vc?", "quem e vc"] 

    def respond_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower().strip()):
            self.format_msg()
            return self._msg
        else:
            return self.pass_to_next(msg)

    def verify_gatling(self, body: str):
        pattern = r"quem [ée] (vc|voc[e-ê])(\??)"
        verify_regex = re.search(pattern, body)
        if verify_regex:
            return True
        return False

    def format_msg(self):
            self.set_msg(DESCRIPTION_MESSAGE)

    def pass_to_next(self, msg: MsgObject):
        return 

class GetAllKidsVerifier(MsgHandler):
    _handler_name = "lista geral"
    _help_message = f"*{_handler_name}* -> Usado para obter a lista de todas as crianças. \n\n A ordem dos dados é: \n\n Nome da criança | Número do quarto | Pais/responsáveis"
    _brief_desc = "Exibe a lista de todos as crianças."

    def respond_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("Getting all the data from kids...")
            self.format_msg()
            return self._msg
        else:
            return self.pass_to_next(msg)

    def format_msg(self):
        with Session(engine) as session:
            msg = """Lista de todas as crianças \n\n"""
            kids = get_kids(session)    
            for kid in kids:
                msg = msg + f"{kid.name} - {kid.room} - {kid.parent}\n"
            self.set_msg(msg)

    def verify_gatling(self, body: str):
        if body == self._handler_name:
            return True
        return False

    def pass_to_next(self, msg: MsgObject):
        return

class GetFormVerifier(MsgHandler):
    _handler_name = "formulario"
    _help_message = f"*{_handler_name}* -> Use este comando par obter o link do formulário de cadastro."
    _brief_desc = f"Link para o formulário de cadastro"

    def respond_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower().strip()):
            self.format_msg()
            return self._msg
        else:
            return self.pass_to_next(msg)

    def verify_gatling(self, body: str):
        if body == self._handler_name or body == "formulário":
            return True
        return False

    def format_msg(self):
        self.set_msg("Acesse a demo do formulário de cadastro! Acesse o link abaixo e cadastre seu(ua) pequeno(a) \n\nhttps://www.jasonuniverse.com.br/jason-monitoring-demo.html")

    def pass_to_next(self, msg: MsgObject):
        pass

get_all_kids_verifier = GetAllKidsVerifier()
get_form_verifier = GetFormVerifier()
get_who_you_are = GetWhoYouAre()

class HelpVerifier(MsgHandler):
    msg_handlers: list[MsgHandler] = [get_all_kids_verifier, get_form_verifier, get_who_you_are]
    _handler_name = "help"
    _help_message = "Claro! eu lhe mostrarei os comandos! Dica extra: Você pode usar _help nome do comando_ para saber mais sobre ele\n\n"

    def respond_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("A help message received!")
            return self.format_msg(msg)
        else:
            return self.pass_to_next(msg) 

    def format_msg(self, msg: MsgObject):
        help_type_msg = self.find_help_field(msg.body.lower())
        if help_type_msg == self._handler_name:
            self.format_general_message()
        else:
            self.format_other_help_message(help_type_msg)
        return self._msg
        
    def find_help_field(self, body):
        space_index = body.find(" ")
        if is_short_message(space_index):
            return body
        return body[space_index+1:]

    def format_general_message(self):
        print("...general help message")
        self.make_general_help_message()
        self.set_msg(self._help_message)

    def make_general_help_message(self):
        self._help_message = "Claro! eu lhe mostrarei os comandos! Dica extra: Você pode usar help <Nome do comando> para saber mais sobre ele\n\n"
        for handler in self.msg_handlers:
            self._help_message += f"*{handler._handler_name}* -> {handler._brief_desc}\n"

    def format_other_help_message(self, formated_msg):
        print("...not general help message")
        for handler in self.msg_handlers:
            if formated_msg == handler._handler_name:
                print(f"{handler._handler_name}... help message")
                self.set_msg(handler._help_message)

    def verify_gatling(self, body):
        if self.first_word_is_help(body):
            return True
        return False

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

    def pass_to_next(self, msg: MsgObject):
        return


class ComplimentVerifier(MsgHandler):
    help_verifier = HelpVerifier()
    msg_handlers: list[MsgHandler]= [help_verifier, get_all_kids_verifier, get_form_verifier, get_who_you_are]
    __compliment_list = ["oi", "olá", "hello"]
    _msg = ""

    def respond_message(self, msg: MsgObject):
        if self.verify_gatling(msg.body.lower()):
            print("hit the greetings message... processing")
            self.set_msg(f"Olá {msg.name}! Precisa de ajuda? Digite *Help* e eu lhe mostro oque sei fazer por enquanto!")
            return self._msg
        else:
            return self.iterate_trough_handlers(msg)    
            
    def iterate_trough_handlers(self, msg: MsgObject):
        for handler in self.msg_handlers:
            handler_msg = handler.respond_message(msg)
            if handler_msg != None:
                return handler_msg
            if handler_msg == None:
                continue
        return self._not_processed_msg

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

    def pass_to_next(self, msg: MsgObject):
        return super().pass_to_next(msg)

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter


class MessageNotRecognizableAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, input_statement, additional_response_selection_parameters):
        return Statement("Mi dispiace, non sono in grado di interpretare questo messaggio!")

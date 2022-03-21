from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from server.statements.request_statement import RequestStatement


class MessageNotRecognizableAdapter(LogicAdapter):
    notRecognizableMessage = "Mi dispiace, non sono in grado di interpretare questo messaggio!"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        response_statement = RequestStatement(self.notRecognizableMessage, statement.text, True)
        response_statement.confidence = 0.3

        return response_statement

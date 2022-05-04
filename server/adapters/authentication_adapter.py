from chatterbot.logic import LogicAdapter
from server.requests.abstract_request import AbstractRequest
from server.statements.request_statement import RequestStatement
from server.utils.utils import lev_dist


class AuthAdapter(LogicAdapter):
    responseAuthenticationAlreadyDone = "Hai già inserito una chiave d'accesso valida!"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        checkWords = ['autenticazione', 'autenticato', 'accesso']

        if not lev_dist(statement.text.split(), checkWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        apiKey = kwargs.get("api_key", None)

        if apiKey is None or not apiKey:
            response = AbstractRequest.responseUnauthorized
        else:
            response = AuthAdapter.responseAuthenticationAlreadyDone

        response_statement = RequestStatement(
            response,
            statement.text,
            True)

        response_statement.confidence = 1

        return response_statement

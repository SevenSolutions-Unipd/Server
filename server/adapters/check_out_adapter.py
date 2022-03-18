from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from server.utils.statement_apikey import StatementApiKey
from server.requests.check_request import CheckRequest
from server.utils.utils import lev_dist
import requests

class CheckOutAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.prev_statement: str = None
        self.adapter: str = None
        self.request = None
        self.apiKey = None

    def can_process(self, statement):
        if self.adapter is not None:
            return True

        checkWords = ['check-out']

        if not lev_dist(statement.text.split(), checkWords):
            return False

        return True

    def process(self, input_statement, additional_response_selection_parameters):
        if self.adapter is None:
            self.adapter = "CheckOutAdapter"
            self.request = CheckRequest()
            self.prev_statement = None

        if isinstance(input_statement, StatementApiKey) and input_statement.apiKey is not None:
            self.apiKey = input_statement.apiKey

        presence_url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"
        response_presence_url = requests.get(presence_url, headers={"api_key": self.apiKey})
        response_statement = Statement(self.request.controlCheckIn(response_presence_url))

        if response_statement == "":
            return Statement("non sei loggato in nessuna sede")


        response = self.request.parseUserInput(input_statement.text, self.prev_statement)
        self.prev_statement = response

        if self.request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/locations/" + self.request.location + "/presence"

            response_url = requests.delete(url, headers={"api_key": self.apiKey})

            response_statement = Statement(self.request.parseResult(response_url))
            #response_statement.confidence = 0

            self.adapter = None
            self.request = None
            self.prev_statement = None
        else:
            if self.request.isQuitting:
                self.adapter = None
                self.request = None
                self.prev_statement = None

            response_statement = Statement(response)
            #response_statement.confidence = 0

        return response_statement
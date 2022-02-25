from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from server.utils.StatementApiKey import StatementApiKey
from server.requests.workingHoursRequest import WorkingHoursRequest
from server.utils.utils import lev_dist
import requests


class WorkingHoursAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.prev_statement: str = None
        self.adapter: str = None
        self.request = None
        self.apiKey = None

    def can_process(self, statement):
        if self.adapter is not None:
            return True

        hoursWords = ['ore']
        workWords = ['consuntivato', 'registrato', 'fatto']

        if not lev_dist(statement.text.split(), hoursWords):
            return False

        if not lev_dist(statement.text.split(), workWords):
            return False

        return True

    def process(self, input_statement, additional_response_selection_parameters):
        if self.adapter is None:
            self.adapter = "WorkingHoursAdapter"
            self.request = WorkingHoursRequest()
            self.prev_statement = None
            # funziona SOLO CON UNA PERSONA!!

        if isinstance(input_statement, StatementApiKey) and input_statement.apiKey is not None:
            self.apiKey = input_statement.apiKey

        response = self.request.parseUserInput(input_statement.text, self.prev_statement)
        self.prev_statement = response

        if self.request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/projects/" + self.request.project + "/activities/me"

            params = dict()
            if self.request.fromdate is not None:
                params['from'] = self.request.fromdate

            if self.request.todate is not None:
                params['to'] = self.request.todate

            responseUrl = requests.get(url, headers={"api_key": self.apiKey}, params=params)

            response_statement = Statement(self.request.parseResult(responseUrl))
            # response_statement.confidence = 0.1

            self.adapter = None
            self.request = None
            self.prev_statement = None
        else:
            if self.request.isQuitting:
                self.adapter = None
                self.request = None
                self.prev_statement = None

            response_statement = Statement(response)
            # response_statement.confidence = 0.1

        return response_statement

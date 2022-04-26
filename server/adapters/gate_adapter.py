import re

import requests

from chatterbot.logic import LogicAdapter
from server.requests.gate_request import GateRequest
from server.statements.gate_statement import GateStatement
from server.utils.utils import lev_dist


class GateAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        activityWords = ['cancello']
        verbsWords = ['apri', 'aprire']

        statement.text = re.sub("[^a-zA-Z0-9 \n./]", ' ', statement.text)

        if not lev_dist(statement.text.split(), activityWords) or not lev_dist(statement.text.split(), verbsWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        request = GateRequest(
            kwargs.get("location", None),
            kwargs.get("device", "gate")
        )

        response = request.parseUserInput(statement.text, statement.in_response_to, **kwargs)

        if request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/locations/" \
                  + request.location + "/devices/" + request.device + "/status/"

            headers = {
                "api_key": kwargs.get("api_key", ""),
                "Content-type": 'application/json'
            }

            serviceResponse = requests.put(url, headers=headers, json={})

            response = request.parseResult(serviceResponse)
            isRequestProcessed = True
        else:
            isRequestProcessed = True if request.isQuitting else False

        response_statement = GateStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.location,
            request.device)

        response_statement.confidence = 1

        return response_statement

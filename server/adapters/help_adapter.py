import re

import requests

from chatterbot.logic import LogicAdapter
from server.requests.help_request import HelpRequest
from server.statements.help_statement import HelpStatement
from server.utils.utils import lev_dist


class HelpAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['aiuto', 'farmacista', 'help', 'come', 'funziona', 'istruzioni', 'operazioni']

        sanitizedWords = re.sub("[^a-zA-Z0-9 \n./]", ' ', statement.text).split()

        if not lev_dist(sanitizedWords, words):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):

        request = HelpRequest(
            kwargs.get("request", None),
        )

        response = request.parseUserInput(statement.text, statement.in_response_to, **kwargs)

        if request.isReady():
            response = request.parseResult(requests.Response())
            isRequestProcessed = True
        else:
            isRequestProcessed = True if request.isQuitting else False

        response_statement = HelpStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.request)

        response_statement.confidence = 1

        return response_statement

from chatterbot.logic import LogicAdapter
from server.requests.check_request import CheckRequest, controlCheckIn
from server.statements.check_statement import CheckStatement
from server.utils.utils import lev_dist
import requests


class InfoCheckInAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        infoWords = ['fatto', 'eseguito', 'svolto', 'inserito']
        checkWords = ['check-in', 'checkin']

        if not lev_dist(statement.text.split(), infoWords) or not lev_dist(statement.text.split(), checkWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"

        apiKey = kwargs.get("api_key")
        serviceResponse = requests.get(url, headers={"api_key": apiKey})

        location = controlCheckIn(serviceResponse)

        if location is not None:
            response = CheckRequest.responseCheckInAlreadyDone + location
        else:
            response = CheckRequest.responseCheckInNotDone

        response_statement = CheckStatement(
            response,
            statement.text,
            True,
            location)

        response_statement.confidence = 1

        return response_statement

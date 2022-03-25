from chatterbot.logic import LogicAdapter
from server.requests.check_request import CheckRequest
from server.statements.check_statement import CheckStatement
from server.utils.utils import lev_dist
import requests

class InfoCheckInAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        infoWords = ['fatto', 'eseguito', 'effettuato', 'svolto', 'inserito']
        checkWords = ['check-in']

        if not lev_dist(statement.text.split(), infoWords) or not lev_dist(statement.text.split(), checkWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):

        request = CheckRequest(
            kwargs.get("location", None)
        )


        url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"

        apiKey = kwargs.get("api_key")
        serviceResponse = requests.get(url, headers={"api_key": apiKey})

        response = request.controlCheckIn(serviceResponse)
        if response != "":
            response = "Risulti presente nella sede: "+response
        else:
            response = "Non hai effettuato il check-in in alcuna sede o hai già effettuato il check-out"

        isRequestProcessed = True

        response_statement = CheckStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.location)

        response_statement.confidence = 1

        return response_statement
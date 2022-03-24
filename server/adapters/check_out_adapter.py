from chatterbot.logic import LogicAdapter
from server.requests.check_request import CheckRequest
from server.statements.check_statement import CheckStatement
from server.utils.utils import lev_dist
import requests

class CheckOutAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        checkWords = ['check-out']

        if not lev_dist(statement.text.split(), checkWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):

        request = CheckRequest(
            kwargs.get("location", None)
        )

        apiKey = kwargs.get("api_key")

        presence_url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"
        response_presence_url = requests.get(presence_url, headers={"api_key": apiKey})
        response_statement = request.controlCheckIn(response_presence_url)

        if response_statement == "":
            return Statement("non sei loggato in nessuna sede")


        response = request.parseUserInput(statement.text, statement.in_response_to)

        if request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/locations/" + request.location + "/presence"

            serviceResponse = requests.delete(url, headers={"api_key": apiKey})

            response = request.parseResult(serviceResponse)
            isRequestProcessed = True
        else:
            isRequestProcessed = True if request.isQuitting else False

        response_statement = CheckStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.location)

        response_statement.confidence = 1

        return response_statement
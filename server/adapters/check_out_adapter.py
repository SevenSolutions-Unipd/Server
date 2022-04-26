import requests

from chatterbot.logic import LogicAdapter
from server.requests.check_request import CheckRequest, controlCheckIn
from server.statements.check_statement import CheckStatement
from server.utils.utils import lev_dist


class CheckOutAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        checkWords = ['check-out', 'checkout', 'uscendo', 'esco']

        if not lev_dist(statement.text.split(), checkWords) or "?" in statement.text:
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        apiKey = kwargs.get("api_key")

        presence_url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"
        response_presence = requests.get(presence_url, headers={"api_key": apiKey})
        location = controlCheckIn(response_presence)

        if location is None:
            response = CheckRequest.responseCheckInNotDone
        else:
            url = "https://apibot4me.imolinfo.it/v1/locations/" + location + "/presence"
            serviceResponse = requests.delete(url, headers={"api_key": apiKey})

            if serviceResponse.status_code == 204:
                response = "Check-out effettuato con successo nella sede " + location
            else:
                response = "Errore nel check-out"  # da capire come fare bene

        response_statement = CheckStatement(
            response,
            statement.text,
            True,
            location)

        response_statement.confidence = 1

        return response_statement

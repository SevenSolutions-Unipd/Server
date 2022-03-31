from chatterbot.logic import LogicAdapter
from server.requests.check_request import CheckRequest, controlCheckIn
from server.statements.check_statement import CheckStatement
from server.utils.utils import lev_dist
import requests


class CheckInAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        checkWords = ['check-in', 'checkin', 'entrando']

        if not lev_dist(statement.text.split(), checkWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        request = CheckRequest(
            kwargs.get("location", None)
        )

        # check if user already checked in
        apiKey = kwargs.get("api_key")

        presence_url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"
        response_presence = requests.get(presence_url, headers={"api_key": apiKey})
        response_checkin_done = controlCheckIn(response_presence)

        # commentato perche sempre attivo con le api fornite
        #        if response_checkin_done != None:
        #            response = CheckRequest.responseCheckInAlreadyDone + response_checkin_done
        #        else: (tutto il resto)

        response = request.parseUserInput(statement.text, statement.in_response_to, **kwargs)

        # validare la sede prima!

        if request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/locations/" + request.location + "/presence"

            serviceResponse = requests.post(url, headers={"api_key": apiKey})

            response = request.parseResult(serviceResponse)
            isRequestProcessed = True
        else:
            isRequestProcessed = True if request.isQuitting else False

        response_statement = CheckStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.location)

        response_statement.confidence = 0.9

        return response_statement

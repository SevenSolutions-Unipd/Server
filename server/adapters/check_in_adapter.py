import requests

from chatterbot.logic import LogicAdapter
from server.requests.check_request import CheckRequest, controlCheckIn
from server.statements.check_statement import CheckStatement
from server.utils.utils import lev_dist


class CheckInAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        checkWords = ['check-in', 'checkin', 'entrando']

        if not lev_dist(statement.text.split(), checkWords) or "?" in statement.text:
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        request = CheckRequest(
            kwargs.get("location", None)
        )

        # check if user already checked in
        presence_url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"
        response_presence = requests.get(presence_url, headers={"api_key": kwargs.get("api_key", "")})
        response_checkin_done = controlCheckIn(response_presence)

        if response_checkin_done is not None:
            response = CheckRequest.responseCheckInAlreadyDone + response_checkin_done
            isRequestProcessed = True
        else:
            response = request.parseUserInput(statement.text, statement.in_response_to, **kwargs)

            if request.isReady():
                url = "https://apibot4me.imolinfo.it/v1/locations/" + request.location + "/presence"

                headers = {
                    "api_key": kwargs.get("api_key", ""),
                    "Content-type": 'application/json'
                }

                serviceResponse = requests.post(url, headers=headers, json={})

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

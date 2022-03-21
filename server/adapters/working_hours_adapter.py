from chatterbot.logic import LogicAdapter

from server.requests.workinghours_request import WorkingHoursRequest
from server.statements.working_hours_statement import WorkingHoursStatement

from server.utils.utils import lev_dist

import requests


class WorkingHoursAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.apiKey = None

    def can_process(self, statement):
        hoursWords = ['ore']
        workWords = ['consuntivato', 'registrato', 'fatto']

        if not lev_dist(statement.text.split(), hoursWords) or not lev_dist(statement.text.split(), workWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):

        request = WorkingHoursRequest(
            kwargs.get("project", None),
            kwargs.get("fromDate", None),
            kwargs.get("toDate", None)
        )

        response = request.parseUserInput(statement.text, statement.in_response_to)

        if request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/projects/" + request.project + "/activities/me"

            params = dict()
            if request.fromDate is not None:
                params['from'] = request.fromDate

            if request.toDate is not None:
                params['to'] = request.toDate

            apiKey = kwargs.get("api_key")
            serviceResponse = requests.get(url, headers={"api_key": apiKey}, params=params)

            response = request.parseResult(serviceResponse)
            isRequestProcessed = True
        else:
            isRequestProcessed = True if request.isQuitting else False

        response_statement = WorkingHoursStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.project,
            request.fromDate,
            request.toDate)

        response_statement.confidence = 1

        return response_statement

import json
import re
from datetime import datetime

from chatterbot.logic import LogicAdapter

from server.requests.activity_request import ActivityRequest
from server.statements.activity_statement import ActivityStatement
from server.utils.utils import lev_dist

import requests


class ActivityAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        activityWords = ['attività', 'EMT']
        verbsWords = ['consuntivare', 'registrare', 'inserire', 'inserisci']

        statement.text = re.sub("[^a-zA-Z0-9 \n./]", ' ', statement.text)

        if not lev_dist(statement.text.split(), activityWords) or not lev_dist(statement.text.split(), verbsWords):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):

        request = ActivityRequest(
            kwargs.get("project", None),
            kwargs.get("date", datetime.today()),
            kwargs.get("billableHours", None),
            kwargs.get("location", None),
            kwargs.get("description", None)
        )

        response = request.parseUserInput(statement.text, statement.in_response_to, **kwargs)

        if request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/projects/" + request.project + "/activities/me"

            headers = {
                "Content-type": 'application/json',
                "api_key": kwargs.get("api_key")
            }

            serviceResponse = requests.post(url, headers=headers, json=[request.getBody()])
            response = request.parseResult(serviceResponse)

            isRequestProcessed = True
        else:
            isRequestProcessed = True if request.isQuitting else False

        response_statement = ActivityStatement(
            response,
            statement.text,
            isRequestProcessed,
            request.project,
            request.date,
            request.billableHours,
            request.location,
            request.description)

        response_statement.confidence = 1
        return response_statement

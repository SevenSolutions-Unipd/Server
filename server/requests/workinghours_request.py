import re
from datetime import datetime
from typing import Optional

from requests import Response

import requests
from server.requests.abstract_request import AbstractRequest
from server.utils import utils


def extractDate(words: list, flags: list) -> Optional[str]:
    if utils.lev_dist(words, flags):
        typo = utils.lev_dist_str(words, flags)

        if words.index(typo) + 1 < len(words):
            try:
                return datetime \
                    .strptime(words[words.index(typo) + 1], '%d/%m/%Y') \
                    .strftime('%Y-%m-%d')
            except ValueError:
                return None
    return None


class WorkingHoursRequest(AbstractRequest):
    responseProjectMissing = "A quale progetto ti stai riferendo?"
    responseProjectNotFound = "Il progetto che hai cercato non esiste"

    def __init__(self, project=None, fromDate=None, toDate=None, **kwargs):
        super().__init__(**kwargs)

        self.project = project
        self.fromDate = fromDate
        self.toDate = toDate

    def parseUserInput(self, input_statement: str, prev_statement: str, **kwargs) -> str:
        if prev_statement is None:
            sanitizedWords = re.sub("[^a-zA-Z0-9 \n./]", ' ', input_statement).split()

            if utils.lev_dist(sanitizedWords, ['progetto']):
                typo = utils.lev_dist_str(sanitizedWords, ['progetto'])
                match = re.search(typo, input_statement, re.IGNORECASE).group()

                if sanitizedWords.index(match) + 1 < len(sanitizedWords):
                    if not self.validateProject(sanitizedWords[sanitizedWords.index(match) + 1], **kwargs):
                        return "Il progetto che hai inserito non esiste!\n\n" + self.responseProjectMissing
                else:
                    return self.responseProjectMissing

                for i in range(len(sanitizedWords)):
                    sanitizedWords[i] = sanitizedWords[i].lower()

                self.fromDate = extractDate(sanitizedWords, ['dal'])
                self.toDate = extractDate(sanitizedWords, ['al'])

                return "Eseguo azione!"
            else:
                return self.responseProjectMissing
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement.__contains__(self.responseProjectMissing):
                if self.validateProject(input_statement, **kwargs):
                    return "Eseguo azione!"
                else:
                    return "Il progetto che hai inserito non esiste!\n\n" + self.responseProjectMissing

    def isReady(self) -> bool:
        if self.project is not None:
            return True
        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 200 and len(response.json()) > 0:
            strReturn = "Consuntivazioni progetto " + self.project + ":\n\n"
            for record in response.json():
                date = datetime.strptime(record.get('date'), '%Y-%m-%d').date()
                strReturn += date.strftime('%d/%m/%Y') + '\n'
                strReturn += "\tLocalità: " + record.get('location', "non segnalata") + '\n'
                strReturn += "\tOre fatturate: " + str(record.get('billableHours', "non registrate")) + '\n'
                strReturn += "\tNote: " + record.get('note', "none") + '\n'
                strReturn += '\n'

            if not strReturn:
                strReturn = "Non ci sono ancora consuntivazioni per il progetto corrente"
            return strReturn
        elif response.status_code == 401:
            return AbstractRequest.responseUnauthorized
        elif response.status_code == 404 or len(response.json()) == 0:
            return WorkingHoursRequest.responseProjectNotFound
        else:
            return AbstractRequest.responseBad

    def validateProject(self, site: str, **kwargs) -> bool:
        apiKey = kwargs.get("api_key", None)

        if apiKey is not None:
            url = "https://apibot4me.imolinfo.it/v1/projects"

            apiKey = kwargs.get("api_key")
            serviceResponse = requests.get(url, headers={"api_key": apiKey})

            if serviceResponse.status_code == 200:
                projects = []

                # parse projects
                for record in serviceResponse.json():
                    projects.append(record.get('code', None))

                if utils.lev_dist([site], projects):
                    self.project = utils.lev_dist_str_correct_word([site], projects)
                    return True
                else:
                    return False
        else:
            self.project = "NotFound"
            return True

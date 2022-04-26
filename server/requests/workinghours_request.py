import re
from datetime import datetime
from typing import Optional

from requests import Response

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
                    self.project = sanitizedWords[sanitizedWords.index(match) + 1]
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
                self.project = input_statement
                return "Eseguo azione!"

    def isReady(self) -> bool:
        if self.project is not None:
            return True
        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 200:
            strReturn = str()
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
        elif response.status_code == 404:
            return WorkingHoursRequest.responseProjectNotFound
        else:
            return AbstractRequest.responseBad

from requests import Response

from server.requests.requestInterface import RequestInterface
from datetime import datetime
import re

from server.utils import utils


class WorkingHoursRequest(RequestInterface):
    responseProjectMissing = "A quale progetto ti stai riferendo?"

    def __init__(self):
        self.isQuitting = False
        self.project = None
        self.fromdate = None
        self.todate = None

    def parseUserInput(self, input_statement: str, prev_statement: str) -> str:
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

                if utils.lev_dist(sanitizedWords, ['dal']):
                    typo = utils.lev_dist_str(sanitizedWords, ['dal'])
                    self.fromdate = datetime\
                        .strptime(sanitizedWords[sanitizedWords.index(typo) + 1], '%d/%m/%Y')\
                        .strftime('%Y-%m-%d')

                    if utils.lev_dist(sanitizedWords, ['al']):
                        typo = utils.lev_dist_str(sanitizedWords, ['al'])
                        self.todate = datetime\
                            .strptime(sanitizedWords[sanitizedWords.index(typo) + 1], '%d/%m/%Y')\
                            .strftime('%Y-%m-%d')
            else:
                return self.responseProjectMissing
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement == self.responseProjectMissing:
                self.project = input_statement
                return "Eseguo azione!"

    def checkQuitting(self, text: str) -> bool:
        quitWords = ['annulla', 'elimina', 'rimuovi']
        self.isQuitting = True
        return any(text.lower().find(check) > -1 for check in quitWords)

    def isReady(self) -> bool:
        if self.project is not None:
            return True

        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 200:
            strReturn = ""
            for record in response.json():
                date = datetime.strptime(record.get('date'), '%Y-%m-%d').date()
                strReturn += date.strftime('%d/%m/%Y') + '\n'
                strReturn += "\tLocalità: " + record.get('location', "non segnalata") + '\n'
                strReturn += "\tOre fatturate: " + str(record.get('billableHours', "non registrate")) + '\n'
                strReturn += "\tNote: " + record.get('note', "none") + '\n'
                strReturn += '\n'

            return strReturn
        elif response.status_code == 401:
            return "Non sei autorizzato ad accedere a questa risorsa. Per favore effettua il login al link ..."
        else:
            return "Il progetto che hai cercato non esiste"

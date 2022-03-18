from requests import Response
from server.requests.request_interface import RequestInterface
from server.utils import utils
import re

class CheckRequest(RequestInterface):
    responseLocationMissing = "A che sede ti stai riferendo?"

    def __init__(self):
        self.isQuitting = False
        self.location = None
        self.user = None

    def parseUserInput(self, input_statement: str, prev_statement: str) -> str:
        if prev_statement is None:
            sanitizedWords = re.sub("[^a-zA-Z0-9 \n./]", ' ', input_statement).split()

            if utils.lev_dist(sanitizedWords, ['sede']):
                typo = utils.lev_dist_str(sanitizedWords, ['sede'])
                match = re.search(typo, input_statement, re.IGNORECASE).group()

                if sanitizedWords.index(match) + 1 < len(sanitizedWords):
                    self.location = sanitizedWords[sanitizedWords.index(match) + 1]
                else:
                    return self.responseLocationMissing

                for i in range(len(sanitizedWords)):
                    sanitizedWords[i] = sanitizedWords[i].lower()


            else:
                return self.responseLocationMissing
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement == self.responseLocationMissing:
                self.location = input_statement
                return "Eseguo azione!"


    def checkQuitting(self, text: str) -> bool:
        quitWords = ['annulla', 'elimina', 'rimuovi']
        self.isQuitting = True
        return any(text.lower().find(check) > -1 for check in quitWords)

    def isReady(self) -> bool:
        if self.location is not None:
            return True
        return False

    def controlCheckOut(self, response:Response) -> str:
        #if response.status_code == 200:
        record = response.json()
        location = record.get('location', "none")
        if location == "none":
            return "Non è stato effettuato alcun check-In, non è possibile effettuare il check-out."
        else:
            return "ok"
        #elif response.status_code == 401:
        #    return "Non sei autorizzato ad accedere a questa risorsa. Per favore effettua il login al link ..."


    def parseResult(self, response: Response) -> str:
        if response.status_code == 201:
            strReturn = "Check-in effettuato con successo nella sede "
            strReturn += self.location
            return strReturn
        elif response.status_code == 204:
            strReturn = "Check-out effettuato con successo nella sede "
            strReturn += self.location
            return strReturn
        elif response.status_code == 401:
            return "Non sei autorizzato ad accedere a questa risorsa. Per favore effettua il login al link ..."
        else:
            return "La sede inserita non esiste"

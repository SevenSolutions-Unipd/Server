from typing import Optional
from requests import Response
from server.requests.abstract_request import AbstractRequest
from server.utils import utils
import requests
import re


def controlCheckIn(response: Response) -> Optional[str]:
    if response.status_code == 200:
        return response.json()['location']
    else:
        return None


class CheckRequest(AbstractRequest):
    responseLocationWrong = "La sede che hai inserito non esiste!\nIn quale sede vuoi fare il check-in?"
    responseLocationMissing = "In quale sede vuoi fare il check-in?"
    responseCheckInAlreadyDone = "Hai già fatto il check-in nella sede di "
    responseCheckInNotDone = "Non hai ancora effettuato il check-in!"

    def __init__(self, location: str = None, **kwargs):
        super().__init__(**kwargs)
        self.location = location

    def parseUserInput(self, input_statement: str, prev_statement: str, **kwargs) -> str:
        if prev_statement is None:
            sanitizedWords = re.sub("[^a-zA-Z0-9 \n./]", ' ', input_statement).split()

            if utils.lev_dist(sanitizedWords, ['sede']):
                typo = utils.lev_dist_str(sanitizedWords, ['sede'])
                match = re.search(typo, input_statement, re.IGNORECASE).group()

                if sanitizedWords.index(match) + 1 < len(sanitizedWords):
                    if self.validateLocation(sanitizedWords[sanitizedWords.index(match) + 1], **kwargs):
                        return "Eseguo azione!"
                    else:
                        return CheckRequest.responseLocationWrong
                else:
                    return CheckRequest.responseLocationMissing
            else:
                return CheckRequest.responseLocationMissing
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement.__contains__(self.responseLocationMissing):
                if self.validateLocation(input_statement, **kwargs):
                    return "Eseguo azione!"
                else:
                    return CheckRequest.responseLocationWrong

    def isReady(self) -> bool:
        if self.location is not None:
            return True
        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 204:
            return "Check-in effettuato con successo nella sede " + self.location
        elif response.status_code == 401:
            return AbstractRequest.responseUnauthorized
        elif response.status_code == 404:
            return "La sede inserita non esiste"
        else:
            return AbstractRequest.responseBad

    def validateLocation(self, site: str, **kwargs) -> bool:
        apiKey = kwargs.get("api_key", None)

        if apiKey is not None:
            url = "https://apibot4me.imolinfo.it/v1/locations"

            apiKey = kwargs.get("api_key")
            serviceResponse = requests.get(url, headers={"api_key": apiKey})

            if serviceResponse.status_code == 200:
                locations = []

                # parse locations
                for record in serviceResponse.json():
                    locations.append(record.get('name', None))

                if utils.lev_dist([site], locations):
                    self.location = utils.lev_dist_str_correct_word([site], locations)
                    return True
                else:
                    return False
        else:
            self.location = "NotFound"
            return True

import re

import requests
from requests import Response

from server.requests.abstract_request import AbstractRequest
from server.utils import utils


class GateRequest(AbstractRequest):
    responseLocationWrong = "La sede che hai inserito non esiste!\nIn quale sede vuoi aprire il cancello?"
    responseLocationMissing = "Di quale sede vuoi aprire il cancello?"

    def __init__(self, location: str = None, device: str = "gate", **kwargs):
        super().__init__(**kwargs)
        self.location = location
        self.device = device

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
                        return GateRequest.responseLocationWrong
                else:
                    return GateRequest.responseLocationMissing
            else:
                return GateRequest.responseLocationMissing
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement.__contains__(self.responseLocationMissing) \
                    or prev_statement.__contains__(self.responseLocationWrong):
                if self.validateLocation(input_statement, **kwargs):
                    return "Eseguo azione!"
                else:
                    return GateRequest.responseLocationWrong

    def isReady(self) -> bool:
        if self.location is not None:
            return True
        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 204:
            return "Cancello aperto con successo nella sede " + self.location
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

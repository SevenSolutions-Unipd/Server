from requests import Response

from server.utils.utils import lev_dist


class AbstractRequest:
    responseUnauthorized = "Non risulti ancora autenticato. Per favore effettua il login sul sito " \
                           "di <a href=\"https://www.imolainformatica.it/\" target=\"_blank\">Imola Informatica</a> " \
                            "ed inserisci la chiave di accesso nelle impostazioni!"
    responseBad = "Qualcosa è andato storto! :("

    def __init__(self, **kwargs):
        self.isQuitting = False

    def checkQuitting(self, text: str) -> bool:
        quitWords = ['annulla', 'elimina', 'rimuovi', 'stop', 'basta']

        self.isQuitting = True if lev_dist(text.split(), quitWords) else False
        return self.isQuitting

    def isQuitting(self) -> bool:
        return self.isQuitting

    def isReady(self) -> bool:
        """Check if the object is ready to process the request"""
        pass

    def parseUserInput(self, input_statement: str, prev_statement: str, **kwargs) -> str:
        """Parse user input to find out if new infos are available"""
        pass

    def parseResult(self, response: Response) -> str:
        """Parse the JSON result of the HTTP Request"""
        pass

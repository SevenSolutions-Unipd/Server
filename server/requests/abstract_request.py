from requests import Response

from server.utils.utils import lev_dist


class AbstractRequest:
    responseUnauthorized = "Non sei autorizzato ad accedere a questa risorsa. Per favore effettua il login al link ..."
    responseBad = "Qualcosa è andato storto :("

    def __init__(self, **kwargs):
        self.isQuitting = None

    def checkQuitting(self, text: str) -> bool:
        quitWords = ['annulla', 'elimina', 'rimuovi']
        self.isQuitting = True

        return lev_dist(text.split(), quitWords)

    def isQuitting(self) -> bool:
        return self.isQuitting

    def isReady(self) -> bool:
        """Check if the object is ready to process the request"""
        pass

    def parseUserInput(self, input_statement: str, prev_statement: str) -> str:
        """Parse user input to find out if new infos are available"""
        pass

    def parseResult(self, response: Response) -> str:
        """Parse the JSON result of the HTTP Request"""
        pass

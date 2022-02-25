from requests import Response


class RequestInterface:
    def __init__(self, **kwargs):
        self.quitting = None

    def isQuitting(self):
        return self.isQuitting

    def isReady(self) -> bool:
        """Check if the object is ready for the request"""
        pass

    def parseUserInput(self, input_statement: str, prev_statement: str) -> str:
        """Parse user input to find out if new infos are available"""
        pass

    def parseResult(self, response: Response) -> str:
        """Parse the JSON result of the HTTP Request"""
        pass

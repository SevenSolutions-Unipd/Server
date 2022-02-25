from chatterbot.conversation import Statement


class StatementApiKey(Statement):
    def __init__(self, text, apiKey, in_response_to=None, **kwargs):
        super(StatementApiKey, self).__init__(text, in_response_to, **kwargs)
        self.apiKey = apiKey

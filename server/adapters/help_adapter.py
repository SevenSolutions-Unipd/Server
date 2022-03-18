from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from server.statements.request_statement import RequestStatement
from server.utils.utils import lev_dist
import re


class HelpAdapter(LogicAdapter):
    helpResponse = "Per sapere le ore che hai registrato puoi mandarmi un messaggio del tipo: \"Quante ore ho " \
                   "consuntivato nel progetto ***?\" Se ti interessa un particolare arco temporale puoi aggiungerlo " \
                   "alla richiesta indicando \"dal gg/mm/aaaa al gg/mm/aaaa\""

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.adapter = None

    def can_process(self, statement):
        if self.adapter is not None:
            return True

        words = ['aiuto', 'farmacista', 'help', 'come', 'funziona', 'istruzioni']

        sanitizedWords = re.sub("[^a-zA-Z0-9 \n./]", ' ', statement.text).split()

        if not lev_dist(sanitizedWords, words):
            return False

        return True

    def process(self, statement, additional_response_selection_parameters=None, **kwargs):
        response_statement = RequestStatement(self.helpResponse, statement.text, True)
        response_statement.confidence = 0.5

        return response_statement

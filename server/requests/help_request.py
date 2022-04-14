from requests import Response
from server.requests.abstract_request import AbstractRequest
from server.utils import utils


class HelpRequest(AbstractRequest):
    availableRequests = [
        "Effettuare il check-in",
        "Effettuare il check-out",
        "Controllo lo stato del check-in",
        "Consuntivare un'attività",
        "Recuperare le attività consuntivate"
    ]

    responseRequestMissing = "Quale funzionalità non riesci ad usare? Puoi chiedermi una delle seguenti:\n" \
                             "- 'Effettuare il check-in'\n" \
                             "- 'Effettuare il check-out'\n" \
                             "- 'Controllo lo stato del check-in'\n" \
                             "- 'Consuntivare un'attività'\n" \
                             "- 'Recuperare le attività consuntivate'\n" \
                             "- ..."

    checkinHelp = "Per effettuare il check-in presso una sede puoi mandarmi un messagio del tipo: " \
                  "\"Vorrei fare il check-in nella sede di ***\" dove '***' è la città della sede.\n\n" \
                  "Se preferisci essere guidato nel processo scrivimi \"Vorrei fare il check-in\""

    checkoutHelp = "Per effettuare il check-out presso una sede puoi mandarmi un messagio del tipo: " \
                   "\"Sto uscendo\""

    checkinInfoHelp = "Per sapere se hai già effettuato il check-in in una sede puoi mandarmi un messaggio del tipo: " \
                      "\"Ho già fatto il check-in?\""

    billActivityHelp = "Per inserire un'attività nel sistema EMT puoi mandarmi un messaggio del tipo: " \
                       "\"Registra un'attività\".\n\nIo ti guiderò nella procedura di inserimento :)"

    billabledActivitiesHelp = "Per sapere le ore che hai registrato puoi mandarmi un messaggio del tipo: \"Quante ore " \
                              "ho " \
                              "consuntivato nel progetto ***?\" Se ti interessa un particolare arco temporale puoi " \
                              "aggiungerlo " \
                              "alla richiesta indicando \"dal gg/mm/aaaa al gg/mm/aaaa\".\n\n Se preferisci essere " \
                              "guidato nella ricerca scrivimi \"Vorrei sapere quante ore ho consutivato\""

    def __init__(self, request: str = None, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def parseUserInput(self, input_statement: str, prev_statement: str, **kwargs) -> str:
        if prev_statement is None:
            return self.responseRequestMissing
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement.__contains__(self.responseRequestMissing):
                if utils.lev_dist([input_statement], HelpRequest.availableRequests):
                    self.request = utils.lev_dist_str_correct_word([input_statement], HelpRequest.availableRequests)
                    return "Eseguo azione!"
                else:
                    return "La funzionalità inserita non esiste.\n\n" + HelpRequest.responseRequestMissing

    def isReady(self) -> bool:
        if self.request is not None:
            return True

        return False

    def parseResult(self, response: Response) -> str:
        if self.request == HelpRequest.availableRequests[0]:
            return HelpRequest.checkinHelp
        elif self.request == HelpRequest.availableRequests[1]:
            return HelpRequest.checkoutHelp
        elif self.request == HelpRequest.availableRequests[2]:
            return HelpRequest.checkinInfoHelp
        elif self.request == HelpRequest.availableRequests[3]:
            return HelpRequest.billActivityHelp
        elif self.request == HelpRequest.availableRequests[4]:
            return HelpRequest.billabledActivitiesHelp

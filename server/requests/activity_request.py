from requests import Response

from server.requests.abstract_request import AbstractRequest
from datetime import datetime

from server.utils import utils


class ActivityRequest(AbstractRequest):
    responseProjectRequest = "In quale progetto vuoi inserire l'attività?"
    responseHoursToBill = "Quante ore hai lavorato a questa attività?"
    responseLocationRequest = "Dove hai svolto questa attività?"
    responseNotesRequest = "Se vuoi scrivi una breve descrizione dell'attività, altrimenti scrivi \"avanti\""

    responseProjectNotFound = "Il progetto che hai cercato non esiste"

    responseActivityBilledSuccessfully = "Attività inserita con successo!"

    def __init__(self,
                 project: str = None,
                 date: datetime = None,
                 billableHours: float = None,
                 location: str = None,
                 description: str = None, **kwargs):
        super().__init__(**kwargs)
        self.project = project
        self.date = datetime.strptime(date, '%Y-%m-%d') if date is str else datetime.today()
        self.billableHours = billableHours
        self.location = location
        self.description = description

    def parseUserInput(self, input_statement: str, prev_statement: str, **kwargs) -> str:
        if prev_statement is None:
            return ActivityRequest.responseProjectRequest
        else:
            if self.checkQuitting(input_statement):
                return "Richiesta annullata!"

            if prev_statement.__contains__(ActivityRequest.responseProjectRequest):
                # TODO: controllare se va bene project con spazi, ...
                self.project = input_statement
                return ActivityRequest.responseHoursToBill

            if prev_statement.__contains__(ActivityRequest.responseHoursToBill):
                try:
                    self.billableHours = float(input_statement)
                    return ActivityRequest.responseLocationRequest
                except ValueError:
                    return "Hai inserito le ore in un formato sbagliato! Devi inserire un numero!" \
                           "(l'eventuale separatore deve essere \".\")\n\n" + ActivityRequest.responseHoursToBill

            if prev_statement.__contains__(ActivityRequest.responseLocationRequest):
                if not any(str.isdigit(c) for c in input_statement):
                    self.location = input_statement
                    return ActivityRequest.responseNotesRequest
                else:
                    return "La località non può contenere numeri!\n\n" + ActivityRequest.responseLocationRequest

            if prev_statement.__contains__(ActivityRequest.responseNotesRequest):
                skipWords = ['avanti', 'niente', 'prosegui', 'skip', 'salta']

                if not utils.lev_dist([input_statement], skipWords):
                    self.description = input_statement
                else:
                    self.description = ""

                return "Eseguo azione!"

    def isReady(self) -> bool:
        if self.project is not None and \
                self.billableHours is not None and \
                self.location is not None and \
                self.description is not None:
            return True

        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 204:
            return ActivityRequest.responseActivityBilledSuccessfully
        elif response.status_code == 401:
            return AbstractRequest.responseUnauthorized
        elif response.status_code == 404:
            return ActivityRequest.responseProjectNotFound
        else:
            return AbstractRequest.responseBad

    def getBody(self) -> dict:
        fields = dict()

        fields["date"] = self.date.strftime('%Y-%m-%d')
        fields["billableHours"] = int(self.billableHours)
        fields["travelHours"] = 0
        fields["billableTravelHours"] = 0
        fields["location"] = self.location
        fields["billable"] = True
        fields["note"] = self.description

        return fields

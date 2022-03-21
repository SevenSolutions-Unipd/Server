from server.statements.request_statement import RequestStatement


class WorkingHoursStatement(RequestStatement):
    __slots__ = (
        'project',
        'fromDate',
        'toDate'
    )

    extra_fields = [
        'project',
        'fromDate',
        'toDate'
    ]

    def __init__(self, text, in_response_to=None, isRequestDone=None, project=None, fromDate=None, toDate=None, **kwargs):
        super().__init__(text, in_response_to, isRequestDone, **kwargs)
        self.project = project
        self.fromDate = fromDate
        self.toDate = toDate

    def get_statement_field_names(self):
        return super().get_statement_field_names() + self.extra_fields

from datetime import datetime
from server.statements.request_statement import RequestStatement


class ActivityStatement(RequestStatement):
    __slots__ = (
        'project',
        'date',
        'billableHours',
        'location',
        'description'
    )

    extra_fields = [
        'project',
        'date',
        'billableHours',
        'location',
        'description'
    ]

    def __init__(self,
                 text: str,
                 in_response_to: str = None,
                 isRequestDone: bool = None,
                 project: str = None,
                 date: datetime = None,
                 billableHours: float = None,
                 location: str = None,
                 description: str = None,
                 **kwargs):
        super().__init__(text, in_response_to, isRequestDone, **kwargs)
        self.project = project
        self.date = date
        self.billableHours = billableHours
        self.location = location
        self.description = description

    def get_statement_field_names(self):
        return super().get_statement_field_names() + self.extra_fields

from server.statements.request_statement import RequestStatement


class GateStatement(RequestStatement):
    __slots__ = (
        'location'
        'device'
    )

    extra_fields = [
        'location'
        'device'
    ]

    def __init__(self,
                 text,
                 in_response_to=None,
                 isRequestDone=None,
                 location=None,
                 device=None,
                 **kwargs):
        super().__init__(text, in_response_to, isRequestDone, **kwargs)
        self.location = location
        self.device = "Gate"

    def get_statement_field_names(self):
        return super().get_statement_field_names() + self.extra_fields

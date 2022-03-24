from server.statements.request_statement import RequestStatement


class CheckStatement(RequestStatement):
    __slots__ = (
        'location'
    )

    extra_fields = [
        'location'
    ]

    def __init__(self, text, in_response_to=None, isRequestDone=None, location=None, **kwargs):
        super().__init__(text, in_response_to, isRequestDone, **kwargs)
        self.location = location

    def get_statement_field_names(self):
        return super().get_statement_field_names() + self.extra_fields
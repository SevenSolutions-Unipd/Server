from server.statements.request_statement import RequestStatement


class HelpStatement(RequestStatement):
    __slots__ = (
        'request'
    )

    extra_fields = [
        'request'
    ]

    def __init__(self, text, in_response_to=None, isRequestDone=None, request=None, **kwargs):
        super().__init__(text, in_response_to, isRequestDone, **kwargs)
        self.request = request

    def get_statement_field_names(self):
        return super().get_statement_field_names() + self.extra_fields

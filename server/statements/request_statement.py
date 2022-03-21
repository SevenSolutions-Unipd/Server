from chatterbot.conversation import Statement


class RequestStatement(Statement):
    __slots__ = (
        'isRequestProcessed'
    )

    extra_fields = [
        'isRequestProcessed'
    ]

    def __init__(self, text, in_response_to=None, isRequestDone=None, **kwargs):
        super().__init__(text, in_response_to, **kwargs)
        self.isRequestProcessed = isRequestDone

    def get_statement_field_names(self):
        return super().get_statement_field_names() + self.extra_fields

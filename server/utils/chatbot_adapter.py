from datetime import datetime

from chatterbot import ChatBot
from chatterbot.conversation import Statement

from server import settings


class ChatBotAdapter:
    def __init__(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)

    def getResponse(self, session, statement: Statement = None, **kwargs) -> Statement:
        if isinstance(statement, str):
            kwargs['text'] = statement

        if isinstance(statement, dict):
            kwargs.update(statement)

        text = kwargs.pop('text')
        input_statement = Statement(text=text, **kwargs)
        kwargs.clear()

        result = None

        if "adapter" not in session:
            # new request
            max_confidence = -1
            kwargs["api_key"] = session["api_key"]

            for adapter in self.chatterbot.logic_adapters:
                if adapter.can_process(input_statement):
                    output = adapter.process(input_statement, None, **kwargs)

                    if output.confidence > max_confidence:
                        session["adapter"] = adapter.class_name
                        result = output
                        max_confidence = output.confidence
        else:
            # request processing already started
            kwargs = session.get("statement")
            kwargs["api_key"] = session["api_key"]

            input_statement.in_response_to = kwargs.pop("text")

            for adapter in self.chatterbot.logic_adapters:
                if adapter.class_name == session.get("adapter"):
                    result = adapter.process(input_statement, None, **kwargs)
                    break

        if result.isRequestProcessed:
            if "adapter" in session:
                session.pop("adapter")

            if "statement" in session:
                session.pop("statement")
        else:
            data = result.serialize()

            for field in data:
                if isinstance(data[field], datetime):
                    data[field] = str(data[field])

            session["statement"] = data

        return result

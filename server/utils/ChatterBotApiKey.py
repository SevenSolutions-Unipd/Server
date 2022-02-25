from chatterbot.chatterbot import ChatBot
from server.utils.StatementApiKey import StatementApiKey


class ChatterBotApiKey(ChatBot):

    def __init__(self, name, **kwargs):
        super(ChatterBotApiKey, self).__init__(name, **kwargs)

    def get_response(self, apiKey, statement=None, **kwargs):

        Statement = self.storage.get_object('statement')

        additional_response_selection_parameters = kwargs.pop('additional_response_selection_parameters', {})

        persist_values_to_response = kwargs.pop('persist_values_to_response', {})

        if isinstance(statement, str):
            kwargs['text'] = statement

        if isinstance(statement, dict):
            kwargs.update(statement)

        if statement is None and 'text' not in kwargs:
            raise self.ChatBotException(
                'Either a statement object or a "text" keyword '
                'argument is required. Neither was provided.'
            )

        if hasattr(statement, 'serialize'):
            kwargs.update(**statement.serialize())

        tags = kwargs.pop('tags', [])

        text = kwargs.pop('text')

        if apiKey is not None:
            input_statement = StatementApiKey(apiKey=apiKey, text=text, **kwargs)
        else:
            input_statement = Statement(text=text, **kwargs)

        input_statement.add_tags(*tags)

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(input_statement)

        # Make sure the input statement has its search text saved

        if not input_statement.search_text:
            input_statement.search_text = self.storage.tagger.get_text_index_string(input_statement.text)

        if not input_statement.search_in_response_to and input_statement.in_response_to:
            input_statement.search_in_response_to = self.storage.tagger.get_text_index_string(
                input_statement.in_response_to)

        response = self.generate_response(input_statement, additional_response_selection_parameters, **kwargs)

        # Update any response data that needs to be changed
        if persist_values_to_response:
            for response_key in persist_values_to_response:
                response_value = persist_values_to_response[response_key]
                if response_key == 'tags':
                    input_statement.add_tags(*response_value)
                    response.add_tags(*response_value)
                else:
                    setattr(input_statement, response_key, response_value)
                    setattr(response, response_key, response_value)

        if not self.read_only:
            self.learn_response(input_statement)

            # Save the response generated for the input
            self.storage.create(**response.serialize())

        return response

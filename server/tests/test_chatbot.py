from server.tests.base_case import ChatterBotTestCase
from server.requests.workinghours_request import WorkingHoursRequest
from server.adapters.msg_notrecognizable_adapter import MessageNotRecognizableAdapter


class ChatBotTests(ChatterBotTestCase):

    def test_get_response_text(self):
        self.chatbot.get_response(text='Test')

    def test_message_not_recognizable(self):
        """
        If statement is not recognizable by the chatbot,
        then return unknown message template
        """
        statement_text = 'Pomodori rossi!!'
        response = self.chatbot.get_response(text=statement_text)

        self.assertEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)
        self.assertEqual(response.confidence, 0)

    def test_working_hours_generic_wrong_project(self):
        """
        If statement is not recognizable by the chatbot,
        then return unknown message template
        """
        statement_text = 'Quante ore ho consuntivato?'
        response = self.chatbot.get_response(text=statement_text)

        if response.text == WorkingHoursRequest.responseProjectMissing:
            statement_text = 'Reana'
            response = self.chatbot.get_response(text=statement_text)

        self.assertEqual(response.text, WorkingHoursRequest.responseProjectNotFound)
        # self.assertEqual(response.confidence, 0)

    def test_working_hours_generic_no_apikey(self):
        """
        If statement is not recognizable by the chatbot,
        then return unknown message template
        """
        statement_text = 'Quante ore ho consuntivato?'
        response = self.chatbot.get_response(text=statement_text)

        if response.text == WorkingHoursRequest.responseProjectMissing:
            statement_text = 'BOT4ME'
            response = self.chatbot.get_response(text=statement_text)

        self.assertEqual(response.text, WorkingHoursRequest.responseUnauthorized)
        # self.assertEqual(response.confidence, 0)

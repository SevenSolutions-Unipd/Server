from unittest import TestCase

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from server import settings
from server.adapters.info_check_in_adapter import InfoCheckInAdapter


class InfoCheckInAdapterTest(TestCase):
    def setUp(self):
        self.chatbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = InfoCheckInAdapter(self.chatbot)
        self.statement = Statement(None)

    def test_can_process_info_check_in(self):
        # TU-17
        """Test if this adapter can process a correct instance"""
        check_statements = ['Ho fatto il check-in?', 'non ricordo se ho eseguito il check-in', 'ho inserito il check-in?']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_info_check_in(self):
        # TU-18
        """Test if this adapter refuse a wrong instance"""
        check_statements = ['Quante ore ho consuntivato oggi?', 'vorrei uscire', 'ciao', 'something']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_info_check_in(self):
        # TI-5
        """Test if this adapter can process an instance with every information"""
        self.statement.text = 'Ho fatto il check-in'
        apikey = '12345678-1234-1234-1234-123456789012'
        response = self.adapter.process(self.statement, api_key=apikey)
        self.assertEqual(response.text, "Non hai ancora effettuato il check-in!")
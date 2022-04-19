from unittest import TestCase
from chatterbot import ChatBot
from server import settings
from server.adapters.check_in_adapter import CheckInAdapter
from chatterbot.conversation import Statement


class CheckInAdapterTest(TestCase):
    def setUp(self):
        self.chatbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = CheckInAdapter(self.chatbot)
        self.statement = Statement(None)

    def test_can_process_ok(self):
        """Test if this adapter can process a correct instance"""
        check_statements = ['Vorrei fare il check-in', 'checkin', 'sto entrando']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_can_process_not_ok(self):
        """Test if this adapter refuse a wrong instance"""
        check_statements = ['check-out', 'vorrei uscire', 'ciao', 'something']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

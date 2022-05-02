from unittest import TestCase

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from server import settings
from server.adapters.check_out_adapter import CheckOutAdapter


class CheckOutAdapterTest(TestCase):
    def setUp(self):
        self.chatbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = CheckOutAdapter(self.chatbot)
        self.statement = Statement(None)

    def test_can_process_check_out(self):
        # TU-13
        """Test if this adapter can process a correct instance"""
        check_statements = ['Vorrei fare il check-out', 'checkout', 'sto uscendo', 'esco']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_check_out(self):
        # TU-14
        """Test if this adapter refuse a wrong instance"""
        check_statements = ['check-in', 'sto entrando', 'ciao', 'something']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_check_out(self):
        # TI-2
        """Test if this adapter can process an instance with every information"""
        self.statement.text = 'Vorrei fare il check-out'
        apikey = '12345678-1234-1234-1234-123456789012'
        response = self.adapter.process(self.statement, api_key=apikey)
        self.assertEqual(response.text, "Check-out effettuato con successo dalla sede IMOLA")

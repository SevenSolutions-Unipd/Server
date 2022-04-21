from unittest import TestCase, mock
from unittest.mock import Mock, patch
from chatterbot import ChatBot
from server import settings
from server.adapters.check_in_adapter import CheckInAdapter
from chatterbot.conversation import Statement


class CheckInAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = CheckInAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_check_in(self):
        # TU-1
        """Test if this adapter can process a correct instance"""
        check_statements = ['Vorrei fare il check-in', 'checkin', 'sto entrando', 'check in']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_check_in(self):
        # TU-2
        """Test if this adapter refuse a wrong instance"""
        check_statements = ['check-out', 'vorrei uscire', 'ciao', 'something']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_check_in(self):
        # TU-9
        """Test if this adapter can process an instance with every information"""
        self.statement.text = 'Vorrei fare il check-in in sede IMOLA'
        response = self.adapter.process(self.statement)
        self.assertEqual(response, "Check-in effettuato con successo nella sede IMOLA")

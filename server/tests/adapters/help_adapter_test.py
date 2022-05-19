from unittest import TestCase
from unittest.mock import patch

from chatterbot.conversation import Statement
from server.adapters.help_adapter import HelpAdapter
from server.requests.help_request import HelpRequest
from server.statements.help_statement import HelpStatement


class HelpAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = HelpAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_help(self):
        # TU-36
        """Test if this adapter can process a correct instance"""
        help_statements = ['Dammi un aiuto', 'help', 'come', 'funziona', 'istruzioni']
        for word in help_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_help(self):
        # TU-37
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['check-out', 'Vorrei consuntivare un\'attività', 'ciao', 'something', 'buonasera']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_help_ok(self):
        # TI-8
        """Test if this adapter can process an instance with every information"""
        apikey = '12345678-1234-1234-1234-123456789012'
        self.statement = HelpStatement("Effettuare il check-in")
        response = self.adapter.process(self.statement, api_key=apikey, request="Effettuare il check-in")
        self.assertEqual(response.text, HelpRequest.checkinHelp)

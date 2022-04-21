from unittest import TestCase, mock
from unittest.mock import Mock, patch
from chatterbot import ChatBot
from server import settings
from server.adapters.help_adapter import HelpAdapter
from chatterbot.conversation import Statement


class HelpAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = HelpAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_help(self):
        """Test if this adapter can process a correct instance"""
        help_statements = ['Dammi un aiuto', 'farmacista', 'help', 'come', 'funziona', 'istruzioni']
        for word in help_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_activity(self):
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['check-out', 'Vorrei consuntivare un\'attività', 'ciao', 'something', 'buonasera']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

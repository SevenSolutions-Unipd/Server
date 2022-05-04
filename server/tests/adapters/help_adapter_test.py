from unittest import TestCase
from unittest.mock import patch

from chatterbot.conversation import Statement
from server.adapters.help_adapter import HelpAdapter


class HelpAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = HelpAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_help(self):
        # TU-36
        """Test if this adapter can process a correct instance"""
        help_statements = ['Dammi un aiuto', 'farmacista', 'help', 'come', 'funziona', 'istruzioni']
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


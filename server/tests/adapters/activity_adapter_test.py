from unittest import TestCase, mock
from unittest.mock import Mock, patch
from chatterbot import ChatBot
from server import settings
from server.adapters.activity_adapter import ActivityAdapter
from chatterbot.conversation import Statement


class ActivityAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = ActivityAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_activity(self):
        """Test if this adapter can process a correct instance"""
        activity_statements = ['Vorrei consuntivare un\'attività', 'Voglio registrare nell\'EMT', 'Registrare nell\'EMT un\'attività']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_activity(self):
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['check-out', 'sto entrando', 'ciao', 'something', 'buonasera']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

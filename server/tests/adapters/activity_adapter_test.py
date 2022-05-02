from unittest import TestCase
from unittest.mock import patch

from chatterbot.conversation import Statement
from server.statements.activity_statement import ActivityStatement
from server.adapters.activity_adapter import ActivityAdapter


class ActivityAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = ActivityAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_activity(self):
        # TU-22
        """Test if this adapter can process a correct instance"""
        activity_statements = ['Vorrei consuntivare un\'attività', 'Voglio registrare nell\'EMT', 'Registrare nell\'EMT un\'attività']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_activity(self):
        # TU-23
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['check-out', 'sto entrando', 'ciao', 'something', 'buonasera']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_activity(self):
        # TI-3
        """Test if this adapter can process an instance with every information"""
        apikey = '12345678-1234-1234-1234-123456789012'
        self.statement = ActivityStatement('registra attività', 'Se vuoi scrivi una breve descrizione dell\'attività, altrimenti scrivi "avanti"', False, 'bot4me', None, 5, 'imola', 'description')
        response = self.adapter.process(self.statement, api_key=apikey)
        self.assertEqual(response.text, "Eseguo azione!")
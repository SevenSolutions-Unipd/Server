from unittest import TestCase
from unittest.mock import patch

from chatterbot.conversation import Statement
from server.adapters.authentication_adapter import AuthAdapter
from server.requests.abstract_request import AbstractRequest
from server.statements.activity_statement import ActivityStatement
from server.adapters.activity_adapter import ActivityAdapter
from server.statements.help_statement import HelpStatement


class AuthAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = AuthAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_activity(self):
        # TU-73
        """Test if this adapter can process a correct instance"""
        activity_statements = ['Sono autenticato?', 'Ho fatto l\' accesso?', 'Mi devo autenticare?']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_activity(self):
        # TU-74
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['sono connesso', 'ehilà sono registrato?', 'aiuto']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_activity_ok(self):
        # TI-7
        """Test if this adapter can process an instance with every information"""
        apikey = '12345678-1234-1234-1234-123456789012'
        response = self.adapter.process(self.statement, api_key=apikey)
        self.assertEqual(response.text, "Hai già inserito una chiave d'accesso valida!")

    def test_process_activity_bad(self):
        # TI-7
        """Test if this adapter can process an instance with every information"""
        response = self.adapter.process(self.statement, api_key="")
        self.assertEqual(response.text, AbstractRequest.responseUnauthorized)

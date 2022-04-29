from unittest import TestCase
from unittest.mock import patch
from server.adapters.gate_adapter import GateAdapter
from chatterbot.conversation import Statement


class CheckInAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = GateAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_gate_open(self):
        # TU-1
        """Test if this adapter can process a correct instance"""
        check_statements = ['Apri cancello', 'vorrei aprire il cancello']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_gate_not_open(self):
        # TU-2
        """Test if this adapter refuse a wrong instance"""
        check_statements = ['gatto matto', 'chiudi cancello', 'ciao', 'something']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_process_gate(self):
        # TU-9
        """Test if this adapter can process an instance with every information"""
        self.statement.text = 'Apri cancello'
        response = self.adapter.process(self.statement)
        self.assertEqual(response.text, "Di quale sede vuoi aprire il cancello?")

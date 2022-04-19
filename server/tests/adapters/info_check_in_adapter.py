from unittest import TestCase
from chatterbot import ChatBot
from server import settings
from server.adapters.info_check_in_adapter import InfoCheckInAdapter
from chatterbot.conversation import Statement


class InfoCheckInAdapterTest(TestCase):
    def setUp(self):
        self.chatbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = InfoCheckInAdapter(self.chatbot)
        self.statement = Statement(None)

    def test_can_process_info_check_in(self):
        """Test if this adapter can process a correct instance"""
        check_statements = ['Ho fatto il check-in?', 'non ricordo se ho eseguito il check-in', 'ho inserito il check-in?']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_info_check_in(self):
        """Test if this adapter refuse a wrong instance"""
        check_statements = ['Quante ore ho consuntivato oggi?', 'vorrei uscire', 'ciao', 'something']
        for word in check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

    def test_conflict_check_in(self):
        """Test if this adapter refuse a check-in insertion request"""
        info_check_statements = ['Vorrei fare il check-in', 'checkin', 'sto entrando', 'check in']
        for word in info_check_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)
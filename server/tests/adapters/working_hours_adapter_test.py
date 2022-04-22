from unittest import TestCase, mock
from unittest.mock import Mock, patch
from chatterbot import ChatBot
from server import settings
from server.adapters.working_hours_adapter import WorkingHoursAdapter
from chatterbot.conversation import Statement


class WorkingHoursAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = WorkingHoursAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_working_hours(self):
        # TU-49
        """Test if this adapter can process a correct instance"""
        wh_statements = ['Quante ore ho consuntivato?', 'Quante ore ho registrato', 'Dimmi il quantitativo di ore che ho fatto']
        for word in wh_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_working_hours(self):
        # TU-50
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['check-out', 'check-in', 'ciao', 'something', 'buonasera']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)

from unittest import TestCase
from unittest.mock import patch

from chatterbot.conversation import Statement
from server.adapters.working_hours_adapter import WorkingHoursAdapter
from server.requests.workinghours_request import WorkingHoursRequest


class WorkingHoursAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = WorkingHoursAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_working_hours(self):
        # TU-48
        """Test if this adapter can process a correct instance"""
        wh_statements = ['Quante ore ho consuntivato?', 'Quante ore ho registrato', 'Dimmi il quantitativo di ore che ho fatto']
        for word in wh_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, True)

    def test_cant_process_working_hours(self):
        # TU-49
        """Test if this adapter refuse a wrong instance"""
        activity_statements = ['check-out', 'check-in', 'ciao', 'something', 'buonasera']
        for word in activity_statements:
            self.statement.text = word
            response = self.adapter.can_process(self.statement)
            self.assertEqual(response, False)


    def test_process_working_hours(self):
        # TI-6
        """Test if this adapter can process an instance with every information"""
        self.statement.text = 'Quante ore ho consuntivato?'
        apikey = '12345678-1234-1234-1234-123456789012'
        response = self.adapter.process(self.statement, api_key=apikey)
        self.assertEqual(response.text, "A quale progetto ti stai riferendo?")

    def test_process_working_hours_complete(self):
        # NEW TEST
        """Test if this adapter can process an instance with every information"""
        apikey = '12345678-1234-1234-1234-123456789012'
        response = self.adapter.process(self.statement, api_key=apikey, project="BOT4ME")
        self.assertNotEqual(response.text, WorkingHoursRequest.responseProjectMissing)
        self.assertNotEqual(response.text, WorkingHoursRequest.responseProjectNotFound)

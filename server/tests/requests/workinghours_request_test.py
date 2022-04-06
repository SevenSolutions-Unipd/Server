from unittest import TestCase
from server.requests.workinghours_request import WorkingHoursRequest


class WorkingHoursRequestTest(TestCase):
    def setUp(self):
        self.request = WorkingHoursRequest()

    def test_request_not_ready(self):
        """Test if request is not ready to be processed"""
        self.request.project = None
        self.assertEqual(self.request.isReady(), False)

    def test_request_ready(self):
        """Test if request is ready to be processed"""
        self.request.project = "BOT4ME"
        self.assertEqual(self.request.isReady(), True)

    def test_request_aborted(self):
        """Test if request is aborted after user's request to abort operation"""
        abort_statements = ['annulla operazione', 'stop', 'elimina operazione', 'basta']

        for word in abort_statements:
            self.request.parseUserInput(word, "something")
            self.assertEqual(self.request.isQuitting, True)
            self.request.isQuitting = False

    def test_user_input_only_project(self):
        """Test if message containing only project's name is correctly parsed"""
        input_statement = "BOT4ME"
        prev_statement = self.request.responseProjectMissing

        self.request.parseUserInput(input_statement, prev_statement)
        self.assertIsNotNone(self.request.project)

    def test_user_input_first_message_no_project(self):
        """Test if request tells the user to insert the project, since it's missing in user's first message"""
        input_statement = "Vorrei sapere le ore consuntivate"

        self.assertEqual(self.request.parseUserInput(input_statement, None), WorkingHoursRequest.responseProjectMissing)
        self.assertEqual(self.request.project, None)
        self.assertEqual(self.request.fromDate, None)
        self.assertEqual(self.request.toDate, None)

    def test_user_input_first_message_no_project_name(self):
        """Test if request tells the user to insert the project, given the following conditions:
            - in user's message there is the word 'project'
            - in user's message there isn't project name"""

        input_statement = "Vorrei sapere le ore consuntivate nel progetto"

        self.assertEqual(self.request.parseUserInput(input_statement, None), WorkingHoursRequest.responseProjectMissing)
        self.assertEqual(self.request.project, None)
        self.assertEqual(self.request.fromDate, None)
        self.assertEqual(self.request.toDate, None)

    def test_user_input_first_message_only_project(self):
        """Test if request tells the user that it's ready to be processed"""
        input_statement = "Vorrei sapere le ore consuntivate nel progetto BOT4ME"

        self.assertEqual(self.request.parseUserInput(input_statement, None), "Eseguo azione!")
        self.assertIsNotNone(self.request.project)
        self.assertEqual(self.request.fromDate, None)
        self.assertEqual(self.request.toDate, None)

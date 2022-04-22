from unittest import TestCase
import requests
from server.requests.help_request import *


class HelpRequestTest(TestCase):
    def setUp(self):
        self.request = HelpRequest()

    def test_request_not_ready(self):
        # TU-39
        """Test if request is not ready to be processed"""
        self.request.request = None
        self.assertEqual(self.request.isReady(), False)

    def test_request_ready(self):
        # TU-39
        """Test if request is ready to be processed"""
        self.request.request = "BOT4ME"
        self.assertEqual(self.request.isReady(), True)

    def test_request_aborted(self):
        # TU-40
        """Test if request is aborted after user's request to abort operation"""
        abort_statements = ['annulla operazione', 'stop', 'elimina operazione', 'basta']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "something")
            self.assertTrue(self.request.isQuitting)
            self.assertEqual(response, "Richiesta annullata!")
            self.request.isQuitting = False

    def test_request_not_aborted(self):
        # TU-40
        """Test if request is not aborted as user doesn't require to abort it"""
        abort_statements = ['something', 'bot4me', 'pomodoro', 'gatto matto']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "not important")
            self.assertFalse(self.request.isQuitting)
            self.assertNotEqual(response, "Richiesta annullata!")

    def test_response_request_missing(self):
        # TU-41
        """Test if request tells the user the list of help function"""
        input_statement = ['aiuto', 'farmacista', 'help', 'come', 'funziona', 'istruzioni']
        for word in input_statement:
            self.assertEqual(self.request.parseUserInput(word, None), HelpRequest.responseRequestMissing)

    def test_execute_available_requests(self):
        # TU-42
        """Test if request tells the user if done"""
        prev_statement = HelpRequest.responseRequestMissing
        input_statements = HelpRequest.availableRequests
        for word in input_statements:
            self.assertEqual(self.request.parseUserInput(word, prev_statement), "Eseguo azione!")

    def test_not_execute_available_requests(self):
        # TU-43
        """Test if request tells the user the list of help function"""
        prev_statement = HelpRequest.responseRequestMissing
        availableRequests = [
            "banane",
            "lamponi",
            "gatto matto",
            "vercingetorige"
        ]
        for word in availableRequests:
            self.assertEqual(self.request.parseUserInput(word, prev_statement), "La funzionalità inserita non esiste.\n\n" + HelpRequest.responseRequestMissing)

    def test_response_check_in(self):
        # TU-44
        """Test if request tells the user the instruction for checkin"""
        input_statement = HelpRequest.availableRequests[0]
        prev_statement = HelpRequest.responseRequestMissing
        self.assertEqual(self.request.parseResult(self.request.parseUserInput(input_statement, prev_statement)), HelpRequest.checkinHelp)

    def test_response_check_out(self):
        # TU-45
        """Test if request tells the user the instruction for checkout"""
        input_statement = HelpRequest.availableRequests[1]
        prev_statement = HelpRequest.responseRequestMissing
        self.assertEqual(self.request.parseResult(self.request.parseUserInput(input_statement, prev_statement)), HelpRequest.checkoutHelp)

    def test_response_check_in_info_help(self):
        # TU-46
        """Test if request tells the user checkin info help"""
        input_statement = HelpRequest.availableRequests[2]
        prev_statement = HelpRequest.responseRequestMissing
        self.assertEqual(self.request.parseResult(self.request.parseUserInput(input_statement, prev_statement)), HelpRequest.checkinInfoHelp)

    def test_response_billable_activity(self):
        # TU-47
        """Test if request tells the user the instruction for insert an activity in EMT"""
        input_statement = HelpRequest.availableRequests[3]
        prev_statement = HelpRequest.responseRequestMissing
        self.assertEqual(self.request.parseResult(self.request.parseUserInput(input_statement, prev_statement)), HelpRequest.billActivityHelp)

    def test_response_billable_activity_help(self):
        # TU-48
        """Test if request tells the user the instruction for see the billable hours"""
        input_statement = HelpRequest.availableRequests[4]
        prev_statement = HelpRequest.responseRequestMissing
        self.assertEqual(self.request.parseResult(self.request.parseUserInput(input_statement, prev_statement)),HelpRequest.billabledActivitiesHelp)


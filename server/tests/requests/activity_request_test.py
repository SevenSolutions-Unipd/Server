from unittest import TestCase
import requests
from server.requests.activity_request import *


class ActivityRequestTest(TestCase):
    def setUp(self):
        self.request = ActivityRequest()

    def test_request_not_ready(self):
        """Test if request is not ready to be processed"""
        self.request.project = None
        self.request.billableHours = None
        self.request.location = None
        self.request.description = None
        self.assertEqual(self.request.isReady(), False)

    def test_request_ready(self):
        """Test if request is ready to be processed"""
        self.request.project = "BOT4ME"
        self.request.billableHours = 8
        self.request.location = "Imola"
        self.request.description = "Implementazione di un fantastico bot"
        self.assertEqual(self.request.isReady(), True)

    def test_request_aborted(self):
        """Test if request is aborted after user's request to abort operation"""
        abort_statements = ['annulla operazione', 'stop', 'elimina operazione', 'basta']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "something")
            self.assertTrue(self.request.isQuitting)
            self.assertEqual(response, "Richiesta annullata!")
            self.request.isQuitting = False

    def test_request_not_aborted(self):
        """Test if request is not aborted as user doesn't require to abort it"""
        abort_statements = ['something', 'bot4me', 'pomodoro', 'gatto matto']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "not important")
            self.assertFalse(self.request.isQuitting)
            self.assertNotEqual(response, "Richiesta annullata!")

    def test_response_insert_project(self):
        """Test if request tells the user to insert project"""
        input_statement = "Vorrei inserire un attività"

        self.assertEqual(self.request.parseUserInput(input_statement, None), ActivityRequest.responseProjectRequest)
        self.assertIsNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNone(self.request.billableHours)
        self.assertIsNone(self.request.location)
        self.assertIsNone(self.request.description)

    def test_response_insert_billable_hour(self):
        """Test if request tells the user to insert billable hours"""
        prev_statement = self.request.responseProjectRequest
        input_statement = "BOT4ME"

        self.assertEqual(self.request.parseUserInput(input_statement, prev_statement), ActivityRequest.responseHoursToBill)
        self.assertIsNotNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNone(self.request.billableHours)
        self.assertIsNone(self.request.location)
        self.assertIsNone(self.request.description)

    def test_response_insert_location(self):
        """Test if request tells the user to insert location"""
        prev_statement = self.request.responseHoursToBill
        input_statement = "8"

        self.assertEqual(self.request.parseUserInput(input_statement, prev_statement), ActivityRequest.responseLocationRequest)
        self.assertIsNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNotNone(self.request.billableHours)
        self.assertIsNone(self.request.location)
        self.assertIsNone(self.request.description)

    def test_wrong_billable_hour_format(self):
        """Test if request tells the user billable hour wrong format"""
        prev_statement = self.request.responseHoursToBill
        input_statement = "banane"
        self.assertEqual(self.request.parseUserInput(input_statement, prev_statement), "Hai inserito le ore in un formato sbagliato! Devi inserire un numero!" \
                   "(l'eventuale separatore deve essere \".\")\n\n" + ActivityRequest.responseHoursToBill)
        self.assertIsNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNone(self.request.billableHours)
        self.assertIsNone(self.request.location)
        self.assertIsNone(self.request.description)

    def test_response_insert_description(self):
        """Test if request tells the user to insert notes"""
        prev_statement = self.request.responseLocationRequest
        input_statement = "Padova"

        self.assertEqual(self.request.parseUserInput(input_statement, prev_statement), ActivityRequest.responseNotesRequest)
        self.assertIsNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNone(self.request.billableHours)
        self.assertIsNotNone(self.request.location)
        self.assertIsNone(self.request.description)

    def test_wrong_location_format(self):
        """Test if request tells the user location wrong format"""
        prev_statement = self.request.responseLocationRequest
        input_statement = "Padova56"

        self.assertEqual(self.request.parseUserInput(input_statement, prev_statement), "La località non può contenere numeri!\n\n" \
                         + ActivityRequest.responseLocationRequest)
        self.assertIsNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNone(self.request.billableHours)
        self.assertIsNone(self.request.location)
        self.assertIsNone(self.request.description)

    def test_insert_activity_with_description(self):
        """Test if request tells the user to insert description"""
        prev_statement = self.request.responseNotesRequest
        input_statement = "Implementazione di un fantastico bot"

        self.assertEqual(self.request.parseUserInput(input_statement, prev_statement), "Eseguo azione!")
        self.assertIsNone(self.request.project)
        self.assertIsNotNone(self.request.date)
        self.assertIsNone(self.request.billableHours)
        self.assertIsNone(self.request.location)
        self.assertIsNotNone(self.request.description)

    def test_insert_activity_with_no_description(self):
        """Test if user skip insert description"""
        prev_statement = self.request.responseNotesRequest
        input_statements = ['avanti', 'niente', 'prosegui', 'skip']
        for word in input_statements:
            self.assertEqual(self.request.parseUserInput(word, prev_statement), "Eseguo azione!")

    def test_response_ok(self):
        """Test if API request return correct content"""
        url = "https://apibot4me.imolinfo.it/v1/projects/BOT4ME/activities/me"
        apiKey = "12345678-1234-1234-1234-123456789012"

        serviceResponse = requests.get(url, headers={"api_key": apiKey})
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 200)
        self.assertNotEqual(response, ActivityRequest.responseProjectNotFound)
        self.assertNotEqual(response, ActivityRequest.responseUnauthorized)

    def test_response_project_missing(self):
        """Test if API request return 404, giving wrong project name"""
        url = "https://apibot4me.imolinfo.it/v1/projects/patate/activities/me"
        apiKey = "12345678-1234-1234-1234-123456789012"

        serviceResponse = requests.get(url, headers={"api_key": apiKey})
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 404)
        self.assertEqual(response, ActivityRequest.responseProjectNotFound)

    def test_response_unauthorized(self):
        """Test if API request return 401, giving no api key"""
        url = "https://apibot4me.imolinfo.it/v1/projects/patate/activities/me"

        serviceResponse = requests.get(url)
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 401)
        self.assertEqual(response, ActivityRequest.responseUnauthorized)

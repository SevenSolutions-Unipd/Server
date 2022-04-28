from unittest import TestCase

from server.requests.gate_request import *


class GateRequestTest(TestCase):
    def setUp(self, **kwargs):
        self.request = GateRequest()
        kwargs['api_key'] = "12345678-1234-1234-1234-123456789012"

    def test_request_not_ready(self):
        # TU-64
        """Test if request is not ready to be processed"""
        self.request.location = None
        self.assertEqual(self.request.isReady(), False)

    def test_request_ready(self):
        # TU-64
        """Test if request is ready to be processed"""
        self.request.location = "imola"
        self.assertEqual(self.request.isReady(), True)

    def test_request_aborted(self):
        # TU-65
        """Test if request is aborted after user's request to abort operation"""
        abort_statements = ['annulla operazione', 'stop', 'elimina operazione', 'basta']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "something")
            self.assertTrue(self.request.isQuitting)
            self.assertEqual(response, "Richiesta annullata!")
            self.request.isQuitting = False

    def test_request_not_aborted(self):
        # TU-65
        """Test if request is not aborted as user doesn't require to abort it"""
        abort_statements = ['something', 'imola', 'word', 'test', 'ciao']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "not important")
            self.assertFalse(self.request.isQuitting)
            self.assertNotEqual(response, "Richiesta annullata!")

    def test_user_input_first_message_no_location(self):
        # TU-66
        """Test if request tells the user to insert the location, since it's missing in user's first message"""
        input_statement = "Aprire il cancello"

        self.assertEqual(self.request.parseUserInput(input_statement, None), GateRequest.responseLocationMissing)
        self.assertIsNone(self.request.location)

    def test_user_input_first_message_no_location_name(self):
        # TU-66
        """Test if request tells the user to insert the location, given the following conditions:
            - in user's message there is the word 'site' (sede)
            - in user's message there isn't location name"""

        input_statement = "Aprire il cancello in sede"

        self.assertEqual(self.request.parseUserInput(input_statement, None), GateRequest.responseLocationMissing)
        self.assertIsNone(self.request.location)

    def test_user_input_first_message_only_location(self):
        # TU-67
        """Test if request tells the user that it's ready to be processed"""
        input_statement = "Aprire il cancello in sede imola"

        self.assertEqual(self.request.parseUserInput(input_statement, None), "Eseguo azione!")
        self.assertIsNotNone(self.request.location)

    def test_user_input_first_message_wrong_location(self, **kwargs):
        # TU-68
        """Test if request tells the user that it's ready to be processed"""
        input_statement = "Aprire il cancello in sede toronto"

        self.assertEqual(self.request.parseUserInput(input_statement, None, **kwargs), GateRequest.responseLocationWrong)
        self.assertIsNotNone(self.request.location)

    def test_user_input_only_location(self):
        """Test if message containing only location's name is correctly parsed"""
        input_statement = "imola"
        prev_statement = self.request.responseLocationMissing

        response = self.request.parseUserInput(input_statement, prev_statement)

        self.assertEqual(response, "Eseguo azione!")
        self.assertIsNotNone(self.request.location)

    def test_response_ok(self):
        # TU-69
        """Test if API request return correct content"""
        url = "https://apibot4me.imolinfo.it/v1/locations/imola/presence"
        apiKey = "12345678-1234-1234-1234-123456789012"

        serviceResponse = requests.get(url, headers={"api_key": apiKey})
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 200)
        self.assertNotEqual(response, GateRequest.responseUnauthorized)
        self.assertNotEqual(response, "La sede inserita non esiste")

    def test_response_unauthorized(self):
        # TU-70
        """Test if API request return 401, giving no api key"""
        url = "https://apibot4me.imolinfo.it/v1/locations/imola/presence"

        serviceResponse = requests.get(url)
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 401)
        self.assertEqual(response, GateRequest.responseUnauthorized)


    def test_validate_location_ok(self):
        # TU-71
        """Test if validateLocation() recognizes an existing site"""
        response = self.request.validateLocation('imola')

        self.assertEqual(response, True)

    def test_validate_location_not_ok(self):
        # TU-71
        """Test if validateLocation() doesn't recognize an unexisting site"""
        response = self.request.validateLocation('XXXXXX')

        self.assertEqual(response, False)


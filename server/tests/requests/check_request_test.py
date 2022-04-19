from unittest import TestCase
from server.requests.check_request import CheckRequest


class CheckRequestTest(TestCase):
    def setUp(self):
        self.request = CheckRequest()

    def test_request_not_ready(self):
        """Test if request is not ready to be processed"""
        self.request.location = None
        self.assertEqual(self.request.isReady(), False)

    def test_request_ready(self):
        """Test if request is ready to be processed"""
        self.request.location = "imola"
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
        abort_statements = ['something', 'imola', 'word', 'test', 'ciao']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "not important")
            self.assertFalse(self.request.isQuitting)
            self.assertNotEqual(response, "Richiesta annullata!")

    def test_user_input_first_message_no_location(self):
        """Test if request tells the user to insert the location, since it's missing in user's first message"""
        input_statement = "Vorrei fare il check-in"

        self.assertEqual(self.request.parseUserInput(input_statement, None), CheckRequest.responseLocationMissing)
        self.assertIsNone(self.request.location)

    def test_user_input_first_message_no_location_name(self):
        """Test if request tells the user to insert the location, given the following conditions:
            - in user's message there is the word 'site' (sede)
            - in user's message there isn't location name"""

        input_statement = "Vorrei effettuare il check-in in sede"

        self.assertEqual(self.request.parseUserInput(input_statement, None), CheckRequest.responseLocationMissing)
        self.assertIsNone(self.request.location)

    def test_user_input_first_message_only_location(self):
        """Test if request tells the user that it's ready to be processed"""
        input_statement = "Vorrei effettuare il check-in in sede imola"

        self.assertEqual(self.request.parseUserInput(input_statement, None), "Eseguo azione!")
        self.assertIsNotNone(self.request.location)

    def test_user_input_first_message_wrong_location(self):
        """Test if request tells the user that it's ready to be processed"""
        input_statement = "Vorrei effettuare il check-in in sede toronto"

        self.assertEqual(self.request.parseUserInput(input_statement, None), CheckRequest.responseLocationWrong)
        self.assertIsNotNone(self.request.location)

    def test_user_input_only_project(self):
        """Test if message containing only location's name is correctly parsed"""
        input_statement = "imola"
        prev_statement = self.request.responseLocationMissing

        response = self.request.parseUserInput(input_statement, prev_statement)
        self.assertEqual(response, "Eseguo azione!")
        self.assertIsNotNone(self.request.location)

    def test_response_ok(self):
        """Test if API request return correct content"""
        url = "https://apibot4me.imolinfo.it/v1/locations/imola/presence"
        apiKey = "12345678-1234-1234-1234-123456789012"

        serviceResponse = requests.post(url, headers={"api_key": apiKey})
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 201)
        self.assertNotEqual(response, CheckRequest.responseUnauthorized)
        self.assertNotEqual(response, "La sede inserita non esiste")

    def test_response_unauthorized(self):
        """Test if API request return 401, giving no api key"""
        url = "https://apibot4me.imolinfo.it/v1/locations/toronto/presence"

        serviceResponse = requests.post(url)
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 401)
        self.assertEqual(response, CheckRequest.responseUnauthorized)

    def test_control_check_in(self):
        """Test if request tell the user his actual location, in case he checked-in"""
        url = "https://apibot4me.imolinfo.it/v1/locations/presence/me"
        apiKey = "12345678-1234-1234-1234-123456789012"

        serviceResponse = requests.get(url, headers={"api_key": apiKey})
        response = controlCheckIn(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 200)
        self.assertEqual(response, serviceResponse.json()[0].get('location', None))

    def test_validate_location_ok(self):
        """Test if validateLocation() recognizes an existing site"""
        response = self.request.validateLocation('imola')

        self.assertEqual(response, True)

    def test_validate_location_not_ok(self):
        """Test if validateLocation() doesn't recognize an unexisting site"""
        response = self.request.validateLocation('toronto')

        self.assertEqual(response, False)


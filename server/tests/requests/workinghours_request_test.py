from unittest import TestCase
from server.requests.workinghours_request import *


class WorkingHoursRequestTest(TestCase):
    def setUp(self):
        self.request = WorkingHoursRequest()

    def test_request_not_ready(self):
        # TU-50
        """Test if request is not ready to be processed"""
        self.request.project = None
        self.assertEqual(self.request.isReady(), False)

    def test_request_ready(self):
        # TU-50
        """Test if request is ready to be processed"""
        self.request.project = "BOT4ME"
        self.assertEqual(self.request.isReady(), True)

    def test_request_aborted(self):
        # TU-51
        """Test if request is aborted after user's request to abort operation"""
        abort_statements = ['annulla operazione', 'stop', 'elimina operazione', 'basta']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "something")
            self.assertTrue(self.request.isQuitting)
            self.assertEqual(response, "Richiesta annullata!")
            self.request.isQuitting = False

    def test_request_not_aborted(self):
        # TU-51
        """Test if request is not aborted as user doesn't require to abort it"""
        abort_statements = ['something', 'bot4me', 'pomodoro', 'gatto matto']

        for word in abort_statements:
            response = self.request.parseUserInput(word, "not important")
            self.assertFalse(self.request.isQuitting)
            self.assertNotEqual(response, "Richiesta annullata!")


    def test_user_input_first_message_no_project(self):
        # TU-52
        """Test if request tells the user to insert the project, since it's missing in user's first message"""
        input_statement = "Vorrei sapere le ore consuntivate"

        self.assertEqual(self.request.parseUserInput(input_statement, None), WorkingHoursRequest.responseProjectMissing)
        self.assertIsNone(self.request.project)
        self.assertIsNone(self.request.fromDate)
        self.assertIsNone(self.request.toDate)

    def test_user_input_first_message_no_project_name(self):
        # TU-52
        """Test if request tells the user to insert the project, given the following conditions:
            - in user's message there is the word 'project'
            - in user's message there isn't project name"""

        input_statement = "Vorrei sapere le ore consuntivate nel progetto"

        self.assertEqual(self.request.parseUserInput(input_statement, None), WorkingHoursRequest.responseProjectMissing)
        self.assertIsNone(self.request.project)
        self.assertIsNone(self.request.fromDate)
        self.assertIsNone(self.request.toDate)

    def test_user_input_first_message_only_project(self):
        # TU-53
        """Test if request tells the user that it's ready to be processed"""
        input_statement = "Vorrei sapere le ore consuntivate nel progetto BOT4ME"

        self.assertEqual(self.request.parseUserInput(input_statement, None), "Eseguo azione!")
        self.assertIsNotNone(self.request.project)
        self.assertIsNone(self.request.fromDate)
        self.assertIsNone(self.request.toDate)

    def test_user_input_first_message_project_and_from_date(self):
        # TU-54
        """Test if request tells the user that it's ready to be processed, giving project's name and fromDate"""
        input_statement = "Vorrei sapere le ore consuntivate nel progetto BOT4ME dal 04/01/2022"

        self.assertEqual(self.request.parseUserInput(input_statement, None), "Eseguo azione!")
        self.assertIsNotNone(self.request.project)
        self.assertIsNotNone(self.request.fromDate)
        self.assertIsNone(self.request.toDate)

    def test_user_input_first_message_project_from_to_date(self):
        # TU-55
        """Test if request tells the user that it's ready to be processed, giving project's name, fromDate and toDate"""
        input_statement = "Vorrei sapere le ore consuntivate nel progetto BOT4ME dal 04/01/2022 al 05/01/2022"

        self.assertEqual(self.request.parseUserInput(input_statement, None), "Eseguo azione!")
        self.assertIsNotNone(self.request.project)
        self.assertIsNotNone(self.request.fromDate)
        self.assertIsNotNone(self.request.toDate)

    def test_user_input_only_project(self):
        # TU-56
        """Test if message containing only project's name is correctly parsed"""
        input_statement = "BOT4ME"
        prev_statement = self.request.responseProjectMissing

        response = self.request.parseUserInput(input_statement, prev_statement)
        self.assertEqual(response, "Eseguo azione!")
        self.assertIsNotNone(self.request.project)

    def test_extract_date_correct_format(self):
        # TU-57
        """Test if a date is correctly parsed, according to ISO date format"""
        # setup (prepazione dell'ambiente)
        correctDate = "04/01/2022"
        isoCorrectDate = "2022-01-04"
        input_statement = "vorrei sapere le ore consuntivate dal " + correctDate
        # action
        date = extractDate(input_statement.split(), ["dal"])
        # check
        self.assertEqual(date, isoCorrectDate)

    def test_extract_date_wrong_format(self):
        # TU-58
        """Test if a date is  not correctly parsed, according to ISO date format"""
        # setup (prepazione dell'ambiente)
        correctDate = "04.01.2022"
        isoCorrectDate = "2022-01-04"
        input_statement = "vorrei sapere le ore consuntivate dal " + correctDate
        # action
        date = extractDate(input_statement.split(), ["dal"])
        # check
        self.assertNotEqual(date, isoCorrectDate)

    def test_extract_date_check_word_in_flags(self):
        # TU-57
        """Test if method correctly parse input_statement, giving a correct flag"""
        # setup (prepazione dell'ambiente)
        input_statement = "vorrei sapere le ore consuntivate dal 04/01/2022"

        date = extractDate(input_statement.split(), ["dal"])

        self.assertIsNotNone(date)

    def test_extract_date_check_word_not_in_flags(self):
        # TU-59
        """Test if method correctly parse input_statement, giving a wrong flag"""
        input_statement = "vorrei sapere le ore consuntivate partendo 04/01/2022"

        date = extractDate(input_statement.split(), ["dal"])

        self.assertIsNone(date)

    def test_extract_date_missing_date(self):
        # TU-59
        """Test if method correctly parse input_statement, giving a wrong flag"""
        input_statement = "vorrei sapere le ore consuntivate dal"

        date = extractDate(input_statement.split(), ["dal"])

        self.assertIsNone(date)

    def test_response_ok(self):
        # TU-60
        """Test if API request return correct content"""
        url = "https://apibot4me.imolinfo.it/v1/projects/BOT4ME/activities/me"

        self.request = WorkingHoursRequest("BOT4ME")

        headers = {
            "Content-type": 'application/json',
            "api_key": "12345678-1234-1234-1234-123456789012"
        }

        serviceResponse = requests.get(url, headers=headers)
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 200)
        self.assertNotEqual(response, WorkingHoursRequest.responseProjectNotFound)
        self.assertNotEqual(response, WorkingHoursRequest.responseUnauthorized)
        self.assertNotEqual(response, WorkingHoursRequest.responseBad)

    def test_response_project_missing(self):
        # TU-61
        """Test if API request return 404, giving wrong project name"""
        url = "https://apibot4me.imolinfo.it/v1/projects/patate/activities/me"

        headers = {
            "Content-type": 'application/json',
            "api_key": "12345678-1234-1234-1234-123456789012"
        }

        serviceResponse = requests.get(url, headers=headers)
        self.request.project = "patate"
        response = self.request.parseResult(serviceResponse)

        # self.assertEqual(serviceResponse.status_code, 404)
        self.assertEqual(response, WorkingHoursRequest.responseProjectNotFound)

    def test_response_unauthorized(self):
        # TU-62
        """Test if API request return 401, giving no api key"""
        url = "https://apibot4me.imolinfo.it/v1/projects/patate/activities/me"

        serviceResponse = requests.get(url)
        response = self.request.parseResult(serviceResponse)

        self.assertEqual(serviceResponse.status_code, 401)
        self.assertEqual(response, WorkingHoursRequest.responseUnauthorized)

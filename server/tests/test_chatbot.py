from datetime import datetime

from django.test import TestCase

from server.adapters.authentication_adapter import AuthAdapter
from server.adapters.msg_notrecognizable_adapter import MessageNotRecognizableAdapter
from server.requests.abstract_request import AbstractRequest
from server.requests.activity_request import ActivityRequest
from server.requests.check_request import CheckRequest
from server.requests.gate_request import GateRequest
from server.requests.help_request import HelpRequest
from server.statements.request_statement import RequestStatement
from server.utils.chatbot_adapter import ChatBotAdapter


class ChatBotTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ChatBotTests, cls).setUpClass()
        cls.adapter = ChatBotAdapter()

    def setUp(self):
        self.session = self.client.session
        self.session["api_key"] = "12345678-1234-1234-1234-123456789012"

    def test_user_check_authentication(self):
        # TS-3-F-1, TS-1-F-6, TS-2-F-52
        """Test if the user can understand if he is authenticated or not"""
        userInput = "stato accesso"

        response = self.adapter.getResponse(self.session, userInput)

        self.assertEqual(response.text, AuthAdapter.responseAuthenticationAlreadyDone)

    def test_user_check_authentication_link(self):
        # TS-1-F-2
        """Test if the user can receive the authentication link if not authenticated"""
        userInput = "stato accesso"
        self.session["api_key"] = ""

        response = self.adapter.getResponse(self.session, userInput)

        self.assertEqual(response.text, AbstractRequest.responseUnauthorized)

    def test_user_check_require_auth_during_operation(self):
        # TS-1-F-3, TS-3-F-47
        """Test if the user can receive the authentication link if not authenticated"""
        userInput = "Vorrei sapere le ore consuntivate nel progetto BOT4ME"
        self.session["api_key"] = ""

        response = self.adapter.getResponse(self.session, userInput)

        self.assertEqual(response.text, AbstractRequest.responseUnauthorized)

    def test_user_input_text_message(self):
        # TS-1-F-4
        """Test if user can interaction with chatbot using texting messages"""
        userInput = "Ehi ci sei?"

        response = self.adapter.getResponse(self.session, userInput)

        self.assertIsNotNone(response.text)
        self.assertFalse(not response.text)

    def test_chatbot_understand_request(self):
        # TS-1-F-7
        """Test if chatbot can understand known operations requests"""
        possibleOperations = [
            "Vorrei sapere le ore consuntivate",
            "Vorrei fare il check-in",
            "Sto uscendo",
            "Vorrei inserire un'attività",
            "Ho fatto il check-in?",
            "Apri il cancello",
            "Aiuto",
            "Sono autenticato?"
        ]

        for operation in possibleOperations:
            response = self.adapter.getResponse(self.session, operation)
            self.assertNotEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)

            if "adapter" in self.session:
                del self.session["adapter"]
            if "statement" in self.session:
                del self.session["statement"]

    def test_chatbot_not_understand_request(self):
        # TS-2-F-8
        """Test if chatbot cannot understand unknown operations requests"""
        possibleOperations = [
            "Vorrei inserire una riunione",
            "Vorrei sapere chi c'è in azienda",
            "Vorrei creare un progetto"

        ]

        for operation in possibleOperations:
            response = self.adapter.getResponse(self.session, operation)
            self.assertEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)

    def test_chatbot_request_missing_infos(self):
        # TS-2-F-9
        """Test if chatbot request missing information, given certain user request"""
        uncompletedInputs = [
            "Vorrei sapere le ore consuntivate",
            "Vorrei fare il checkin",
            "Apri il cancello",
            "Aiuto"
        ]

        for sentence in uncompletedInputs:
            response = RequestStatement(self.adapter.getResponse(self.session, sentence))
            self.assertFalse(response.isRequestProcessed)

    def test_chatbot_available_operations_request(self):
        # TS-3-F-10
        """Test if chatbot gives a list of available operations when user requires them"""
        requestInputs = [
            "Aiuto",
            "Operazioni disponibili",
            "Come si usa?",
            "Vorrei un elenco delle operazioni",
            "Farmacista!"
        ]

        for sentence in requestInputs:
            response = self.adapter.getResponse(self.session, sentence)
            self.assertEqual(response.text, HelpRequest.responseRequestMissing)

            if "adapter" in self.session:
                del self.session["adapter"]
            if "statement" in self.session:
                del self.session["statement"]

    def test_chatbot_check_operations(self):
        # TS-1-F-11
        """Test if chatbot correctly detect check-in and check-out requests"""
        checkInputs = [
            "Vorrei fare il check-in",
            "Ho fatto il check-in?",
            "Sto uscendo",
            "Sto entrando"
        ]

        for sentence in checkInputs:
            response = self.adapter.getResponse(self.session, sentence)
            self.assertNotEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)

    def test_chatbot_checkin_response(self):
        # TS-2-F-12
        """Test if chatbot correctly tell the user about the successfully executed check-in operation"""
        user_input = "Vorrei fare il check-in nella sede Imola"

        response = self.adapter.getResponse(self.session, user_input)
        self.assertEqual(response.text, "Check-in effettuato con successo nella sede IMOLA")

    def test_chatbot_checkout_response(self):
        # TS-2-F-12
        """Test if chatbot correctly tell the user about the successfully executed check-out operation"""
        user_input = "Vorrei fare il check-in nella sede Imola"
        self.adapter.getResponse(self.session, user_input)

        user_input = "Sto uscendo"
        response = self.adapter.getResponse(self.session, user_input)
        self.assertEqual(response.text, "Check-out effettuato con successo dalla sede IMOLA")

    def test_chatbot_checkin_complete(self):
        # TS-1-F-13, TS-1-F-50
        """Test if chatbot can correctly detect the location in the first user message"""
        user_input = "Sto entrando nella sede Bologna"
        response = self.adapter.getResponse(self.session, user_input)
        self.assertEqual(response.text, "Check-in effettuato con successo nella sede BOLOGNA")

    def test_chatbot_checkin_missing_location(self):
        # TS-2-F-14
        """Test if the chatbot can understand that the location is missing in the first user message"""
        self.adapter.getResponse(self.session, "sto uscendo")  # delete previous check-in
        user_input = "Sto entrando"
        response = RequestStatement(self.adapter.getResponse(self.session, user_input))

        self.assertEqual(response.text, CheckRequest.responseLocationMissing)
        self.assertFalse(response.isRequestProcessed)

    def test_chatbot_checkin_wrong_location(self):
        # TS-2-F-15
        """Test if the chatbot can detect a wrong location in the user message"""
        self.adapter.getResponse(self.session, "sto uscendo")  # delete previous check-in
        user_input = "Sto entrando nelle sede di Padova"

        response = RequestStatement(self.adapter.getResponse(self.session, user_input))

        self.assertEqual(response.text, CheckRequest.responseLocationWrong)
        self.assertFalse(response.isRequestProcessed)

    def test_chatbot_understand_activity_operation(self):
        # TS-1-F-16
        """Test if chatbot correctly understand that user requires to insert an activity record"""
        activitySentences = [
            "Vorrei inserire un'attività",
            "Inserisci attività",
            "Consuntiva attivita",
            "Registra in emt"
        ]

        for sentence in activitySentences:
            response = self.adapter.getResponse(self.session, sentence)
            self.assertNotEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)

            if "adapter" in self.session:
                del self.session["adapter"]
            if "statement" in self.session:
                del self.session["statement"]

    def test_chatbot_activity_insert_working_hours(self):
        # TS-2-F-17, TS-2-F-23
        """Test if chatbot require working hours after user require to insert an activity record"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        response = RequestStatement(self.adapter.getResponse(self.session, "BOT4ME"))

        self.assertEqual(response.text, ActivityRequest.responseHoursToBill)
        self.assertFalse(response.isRequestProcessed)

    def test_chatbot_activity_insert_notes(self):
        # TS-2-F-18, TS-2-F-23
        """Test if chatbot require activity's notes after user require to insert an activity record"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")
        self.adapter.getResponse(self.session, "4")
        response = RequestStatement(self.adapter.getResponse(self.session, "Padova"))

        self.assertEqual(response.text, ActivityRequest.responseNotesRequest)
        self.assertFalse(response.isRequestProcessed)

    def test_chatbot_activity_insert_location(self):
        # TS-3-F-19, TS-2-F-23
        """Test if chatbot require activity's location after user require to insert an activity record"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")
        response = RequestStatement(self.adapter.getResponse(self.session, "4"))

        self.assertEqual(response.text, ActivityRequest.responseLocationRequest)
        self.assertFalse(response.isRequestProcessed)

    def test_chatbot_activity_insert_working_hours_wrong(self):
        # TS-3-F-20
        """Test if chatbot tells the user that the amount of working hours inserted is invalid"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")

        wrongHours = [
            "quattro",
            "4 ore e mezza",
            "4,5"
        ]

        for sentence in wrongHours:
            response = RequestStatement(self.adapter.getResponse(self.session, sentence))
            self.assertEqual(response.text, "Hai inserito le ore in un formato sbagliato! Devi inserire un numero!" \
                                            "(l'eventuale separatore deve essere \".\")\n\n"
                             + ActivityRequest.responseHoursToBill)
            self.assertFalse(response.isRequestProcessed)

    def test_chatbot_activity_insert_location_wrong(self):
        # TS-3-F-21
        """Test if chatbot tells the user that the location inserted is invalid"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")
        self.adapter.getResponse(self.session, "4")

        wrongLocations = [
            "1mol4",
            "4"
        ]

        for sentence in wrongLocations:
            response = RequestStatement(self.adapter.getResponse(self.session, sentence))
            self.assertEqual(response.text, "La località non può contenere numeri!\n\n"
                             + ActivityRequest.responseLocationRequest)
            self.assertFalse(response.isRequestProcessed)

    def test_chatbot_activity_skip_notes(self):
        # TS-2-F-22, TS-2-F-23
        """Test if chatbot let the user to not insert activity's notes"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")
        self.adapter.getResponse(self.session, "4")
        self.adapter.getResponse(self.session, "Padova")

        response = self.adapter.getResponse(self.session, "avanti")

        self.assertEqual(response.text, ActivityRequest.responseActivityBilledSuccessfully)
        self.assertTrue(response.isRequestProcessed)

    def test_chatbot_activity_inserted_succesfully(self):
        # TS-2-F-24, TS-1-F-50
        """Test if chatbot correctly tells the user that activity has been successfully inserted"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")
        self.adapter.getResponse(self.session, "4")
        self.adapter.getResponse(self.session, "Padova")
        response = self.adapter.getResponse(self.session, "Testing funzionalità")

        self.assertEqual(response.text, ActivityRequest.responseActivityBilledSuccessfully)
        self.assertTrue(response.isRequestProcessed)

    def test_chatbot_activity_inserted_bad(self):
        # TS-2-F-24
        """Test if chatbot correctly tells the user that activity has not been successfully inserted"""
        self.adapter.getResponse(self.session, "Vorrei inserire un'attività")
        self.adapter.getResponse(self.session, "BOT4ME")
        self.adapter.getResponse(self.session, "999")
        self.adapter.getResponse(self.session, "Padova")
        response = self.adapter.getResponse(self.session, "Testing funzionalità")

        self.assertEqual(response.text, AbstractRequest.responseBad)
        self.assertTrue(response.isRequestProcessed)

    def test_chatbot_gate_operation(self):
        # TS-1-F-25, TS-2-F-26, TS-2-F-28, TS-1-F-50
        """Test if chatbot can understand and execute gate opening request"""
        user_input = "Apri cancello sede Imola"

        response = self.adapter.getResponse(self.session, user_input)

        self.assertEqual(response.text, "Cancello aperto con successo nella sede IMOLA")
        self.assertTrue(response.isRequestProcessed)

    def test_chatbot_gate_location_missing(self):
        # TS-2-F-27
        """Test if chatbot can understand and execute gate opening request"""
        user_input = "Apri cancello"

        response = self.adapter.getResponse(self.session, user_input)

        self.assertEqual(response.text, GateRequest.responseLocationMissing)
        self.assertFalse(response.isRequestProcessed)

    def test_chatbot_checkin_status(self):
        # TS-1-F-54
        """Test if chatbot can tell the user about the check-in status"""
        user_input = "Ho fatto il check-in?"

        response = self.adapter.getResponse(self.session, user_input)

        self.assertNotEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)
        self.assertTrue(response.isRequestProcessed)

    def test_chatbot_current_working_hours(self):
        # TS-1-F-55
        """Test if chatbot can retrieve today's working hours, given a project"""
        today = datetime.now().strftime("%d/%m/%Y")
        user_input = "Ore fatte progetto BOT4ME dal " + today + " al " + today

        response = self.adapter.getResponse(self.session, user_input)

        self.assertNotEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)
        self.assertIsNotNone(response.text)
        self.assertTrue(response.isRequestProcessed)

    def test_chatbot_withdraw_operation(self):
        # TS-3-F-58
        """Test if chatbot can withdraw an already-started operation"""
        self.adapter.getResponse(self.session, "Vorrei fare il check-in")

        user_input = "annulla operazione"
        response = self.adapter.getResponse(self.session, user_input)

        self.assertEqual(response.text, "Richiesta annullata!")
        self.assertTrue(response.isRequestProcessed)

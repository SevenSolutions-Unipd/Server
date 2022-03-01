from server.utils.chatterbot_apikey import ChatterBotApiKey
from django.test import TransactionTestCase
from server import settings


class ChatterBotTestCase(TransactionTestCase):

    def setUp(self):
        super().setUp()
        self.chatbot = ChatterBotApiKey(**settings.CHATTERBOT)

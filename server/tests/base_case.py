from django.test import TransactionTestCase

from chatterbot import ChatBot
from server import settings


class ChatterBotTestCase(TransactionTestCase):

    def setUp(self):
        super().setUp()
        self.chatbot = ChatBot(**settings.CHATTERBOT)

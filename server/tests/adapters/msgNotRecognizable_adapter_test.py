from unittest import TestCase
from unittest.mock import patch

from chatterbot.conversation import Statement
from server.adapters.authentication_adapter import AuthAdapter
from server.adapters.msg_notrecognizable_adapter import MessageNotRecognizableAdapter
from server.requests.abstract_request import AbstractRequest
from server.statements.activity_statement import ActivityStatement
from server.adapters.activity_adapter import ActivityAdapter
from server.statements.help_statement import HelpStatement


class MessageNotRecognizableAdapterTest(TestCase):

    @patch("chatterbot.ChatBot")
    def setUp(self, chatbot):
        self.adapter = MessageNotRecognizableAdapter(chatbot)
        self.statement = Statement(None)

    def test_can_process_msg_not_recognizable(self):
        # NEW TEST
        """Test if this adapter can process a correct instance"""
        response = self.adapter.can_process(self.statement)
        self.assertEqual(response, True)

    def test_process_msg_not_recognizable(self):
        # NEW TEST
        """Test if this adapter can process an instance with every information"""
        response = self.adapter.process(self.statement, api_key="")
        self.assertEqual(response.text, MessageNotRecognizableAdapter.notRecognizableMessage)

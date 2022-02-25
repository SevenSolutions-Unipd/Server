import json

from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse
from server.utils.ChatterBotApiKey import ChatterBotApiKey
from chatterbot.ext.django_chatterbot import settings


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


@method_decorator(csrf_exempt, name='dispatch')
class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """
    chatbots = dict()  # NON È THREAD-SAFE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ZIO BOIA!!!!

    # chatterbot = ChatterBotApiKey(**settings.CHATTERBOT)

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'Non è stato specificato nessun testo!'
                ]
            }, status=400)

        if request.headers["Authorization"] is not None:
            apiKey = request.headers["Authorization"]
        else:
            apiKey = None

        # for key, value in self.chatbots.items():
        #    print("POST BEFORE KEY = " + key)

        if request.session.session_key not in self.chatbots:
            # print("Creating chatbot POST")
            self.chatbots[request.session.session_key] = ChatterBotApiKey(**settings.CHATTERBOT)

        # for key, value in self.chatbots.items():
        #    print("POST AFTER KEY = " + key)

        # print("POST REQUEST KEY = " + request.session.session_key)
        response = self.chatbots[request.session.session_key].get_response(apiKey, input_data)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        # for key, value in self.chatbots.items():
        #    print("GET BEFORE KEY = " + key)

        if not request.session.session_key or request.session.session_key not in self.chatbots:
            request.session.create()
            # print("Creating chatbot GET")
            self.chatbots[request.session.session_key] = ChatterBotApiKey(**settings.CHATTERBOT)

        # for key, value in self.chatbots.items():
        #    print("GET AFTER KEY = " + key)

        # print("GET REQUEST KEY = " + request.session.session_key)
        return JsonResponse({
            'text': "Ciao! Io sono Alfredo, il tuo assistente. Se hai bisogno di aiuto scrivimi \"farmacista\" :)",
        }, status=200)

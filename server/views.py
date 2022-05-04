import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.base import TemplateView

from server.utils.chatbot_adapter import ChatBotAdapter


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


@method_decorator(csrf_exempt, name='dispatch')
class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """
    bot = ChatBotAdapter()

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

        if not request.session.session_key:
            request.session.create()

        if "Authorization" in request.headers and request.headers["Authorization"] is not None:
            request.session["api_key"] = request.headers["Authorization"]
        else:
            request.session["api_key"] = None

        response = self.bot.getResponse(request.session, input_data)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """

        if not request.session.session_key:
            request.session.create()

        return JsonResponse({
            'text': "Ciao! Io sono Alfredo, il tuo assistente. Se hai bisogno di aiuto scrivimi \"aiuto\" :)",
        }, status=200)

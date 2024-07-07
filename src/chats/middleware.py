from django.http import HttpResponseServerError
import logging
logger = logging.getLogger("chats")


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response = HttpResponseServerError("Неизвестная ошибка!")
            logger.error(e)
        return response
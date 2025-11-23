import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    """
    Logs every request with:
    - timestamp
    - user (or AnonymousUser)
    - request path
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Configure logger for request logs
        self.logger = logging.getLogger("request_logger")

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        timestamp = datetime.now()

        self.logger.info(f"{timestamp} - User: {user} - Path: {request.path}")

        response = self.get_response(request)

        return response

class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the chats API outside allowed hours.
    Allowed hours: 6 AM to 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allowed window: 6 AM (06:00) to 9 PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted during these hours."
            )

        return self.get_response(request)

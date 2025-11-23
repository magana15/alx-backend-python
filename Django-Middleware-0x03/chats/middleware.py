import logging
from datetime import datetime

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

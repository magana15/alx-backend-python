import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
import threading
from collections import deque
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    """
    Rate-limit POST requests to message endpoints by client IP.

    Behavior:
    - Tracks timestamps of POST requests per IP in an in-memory deque.
    - Default policy: max_messages=5 within window_seconds=60.
    - Applies only to POST requests where the path contains '/messages' (adjust as needed).
    - If limit is exceeded, returns HTTP 429 with a JSON error.
    """

    def __init__(self, get_response, max_messages: int = 5, window_seconds: int = 60):
        self.get_response = get_response
        # Configuration
        self.max_messages = max_messages
        self.window_seconds = window_seconds

        # In-memory store: ip -> deque([timestamp, ...])
        self._store = {}
        # Lock to protect access to _store across threads (development server uses threads).
        self._lock = threading.Lock()

    def _get_client_ip(self, request):
        # Common header used by proxies. If you're behind a proxy set USE_X_FORWARDED_HOST / proper settings.
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            # X-Forwarded-For may be "client, proxy1, proxy2"
            ip = xff.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip or "unknown"

    def _prune_deque(self, dq, now):
        # Remove timestamps older than window_seconds from the left
        cutoff = now - self.window_seconds
        while dq and dq[0] < cutoff:
            dq.popleft()

    def __call__(self, request):
        # Only enforce on POST requests to message endpoints
        if request.method == "POST" and "/messages" in request.path:
            ip = self._get_client_ip(request)
            now = time.time()

            with self._lock:
                dq = self._store.get(ip)
                if dq is None:
                    dq = deque()
                    self._store[ip] = dq

                # prune old entries
                self._prune_deque(dq, now)

                if len(dq) >= self.max_messages:
                    # rate limit exceeded
                    retry_after = int(self.window_seconds - (now - dq[0])) if dq else self.window_seconds
                    body = {
                        "detail": "Rate limit exceeded: too many messages sent. Try again later.",
                        "max_messages": self.max_messages,
                        "window_seconds": self.window_seconds,
                        "retry_after_seconds": max(retry_after, 0),
                    }
                    # 429 Too Many Requests
                    resp = JsonResponse(body, status=429)
                    resp["Retry-After"] = str(body["retry_after_seconds"])
                    return resp

                # record this request
                dq.append(now)

        # For non-matching requests or when under limit, proceed normally
        response = self.get_response(request)

        # Optional: periodic cleanup to avoid unbounded growth (very cheap check)
        # Runs without lock contention for performance; safe to skip in high-load.
        if int(time.time()) % 60 == 0:
            # try a quick cleanup pass
            with self._lock:
                now = time.time()
                to_delete = []
                for ip, dq in self._store.items():
                    self._prune_deque(dq, now)
                    if not dq:
                        to_delete.append(ip)
                for ip in to_delete:
                    del self._store[ip]

        return response


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

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Skip admin site
        if request.path.startswith("/admin"):
            return self.get_response(request)

        # If user is not authenticated, deny
        if not request.user.is_authenticated:
            return JsonResponse(
                {"detail": "Authentication required"},
                status=401
            )

        # Extract role (assuming user model has 'role' attribute)
        role = getattr(request.user, "role", None)

        # Allowed roles
        allowed_roles = ["admin", "moderator"]

        # If not allowed, deny
        if role not in allowed_roles:
            return JsonResponse(
                {"detail": "Forbidden: insufficient role permissions"},
                status=403
            )

        # Continue normal execution
        response = self.get_response(request)
        return response

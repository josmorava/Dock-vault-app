import json
from datetime import timedelta

from django.contrib.auth import logout
from django.http import QueryDict
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.datastructures import MultiValueDict


class JsonPostMiddleware:
    """Inertia sends non-file form submissions as application/json, but Django
    only populates request.POST for form-encoded/multipart bodies. This mirrors
    the JSON body into request.POST so views can read it the usual way."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.method in ("POST", "PUT", "PATCH")
            and request.content_type == "application/json"
            and request.body
        ):
            try:
                data = json.loads(request.body)
            except ValueError:
                data = None
            if isinstance(data, dict):
                query_dict = QueryDict(mutable=True)
                for key, value in data.items():
                    if isinstance(value, list):
                        query_dict.setlist(key, value)
                    else:
                        query_dict[key] = "" if value is None else value
                request._post = query_dict
                request._files = MultiValueDict()
        return self.get_response(request)


class EnsureCsrfCookieMiddleware:
    """Forces the CSRF cookie to be set on every response, since Django only
    sets it lazily when something reads the token (e.g. {% csrf_token %}).
    Inertia's requests rely on the cookie being present from the first page load."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        get_token(request)
        return self.get_response(request)


class SessionActivityMiddleware:
    """Forces logout when a user has been inactive past their configured timeout."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            timeout = timedelta(minutes=user.session_timeout_minutes or 30)
            now = timezone.now()
            if user.last_activity and now - user.last_activity > timeout:
                logout(request)
            else:
                user.last_activity = now
                user.save(update_fields=["last_activity"])
        return self.get_response(request)

from django.contrib.auth import authenticate, login
from django.utils.deprecation import MiddlewareMixin


class OneTimeCodeAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        code = request.GET.get('otcode', None)
        if not code:
            return None

        user = authenticate(code=code)
        if user:
            login(request, user)

        return None

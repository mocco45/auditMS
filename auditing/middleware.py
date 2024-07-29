# auditing/middleware.py
import json
from audit.models import UserActionLog

class UserActionLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            action = f"{request.method} {request.path}"
            description = json.dumps(request.POST) if request.method == 'POST' else ''
            UserActionLog.objects.create(user=request.user, action=action, description=description)
        return response

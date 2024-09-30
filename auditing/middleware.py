# auditing/middleware.py
import json
from audit.models import UserActionLog
from django.utils.deprecation import MiddlewareMixin


class UserActionLogMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            if request.method in ['POST', 'PUT', 'DELETE']:
                action = f"{request.method} {request.path}"
                description = json.dumps(request.POST) if request.method in ['POST', 'PUT'] else ''
                UserActionLog.objects.create(user=request.user, action=action, description=description)
        return response

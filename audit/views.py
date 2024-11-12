from django.shortcuts import render
from django.http import JsonResponse
from .models import UserActionLog
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, "index.html")


@permission_classes([IsAuthenticated])
def user_action_logs(request):
    logs = UserActionLog.objects.filter(user=request.user)
    data = [
        {
            "action": log.action,
            "timestamp": log.timestamp,
            "description": log.description,
        }
        for log in logs
    ]
    return JsonResponse({"status": "success", "logs": data})

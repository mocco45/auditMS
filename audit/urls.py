from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("accounts.urls")),
    path("", include("companies.urls")),
    path("", include("data_manipulation.urls")),
    path("api/user-action-logs/", views.user_action_logs, name="user_action_logs"),
]

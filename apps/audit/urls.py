from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("apps.accounts.urls")),
    path("", include("apps.companies.urls")),
    path("", include("apps.data_manipulation.urls")),
    path("api/user-action-logs/", views.user_action_logs, name="user_action_logs"),
]

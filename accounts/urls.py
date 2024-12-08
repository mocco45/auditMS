from django.urls import path
from . import views

urlpatterns = [
    path("api/create-user/", views.UserCreateView.as_view(), name="create_user"),
    path("api/token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("api/verify/", views.VerifyTokenView.as_view(), name="token_verify"),
    path("api/create-role", views.create_role, name="create_role"),
    path("api/create-permission", views.create_permission, name="create_permission"),
    path("api/assign-role", views.assign_role, name="assign_role"),
    path(
        "api/assign-permission",
        views.assign_permission_to_role,
        name="assign_permission",
    ),
    path("api/users", views.list_user, name="users"),
    path("api/roles", views.list_roles, name="roles"),
    path("api/permissions", views.list_permission, name="permissions"),
    path("api/user/<int:pk>", views.UserDetailsView.as_view(), name="user"),
]

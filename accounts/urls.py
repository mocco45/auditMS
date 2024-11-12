from django.urls import path
from . import views

urlpatterns = [
    path("api/create-user/", views.UserCreateView.as_view(), name="create_user"),
    path("api/token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("api/verify/", views.VerifyTokenView.as_view(), name="token_verify"),
]

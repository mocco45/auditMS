from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CustomUser
from django.contrib.auth.models import Group
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # If the request reaches here, the token is valid
        return Response({"message": "Token is valid"}, status=200)


@api_view(["POST"])
def assign_role(request):
    user_id = request.data.get("user_id")
    role_id = request.data.get("role_id")

    try:
        user = CustomUser.objects.get(id=user_id)
        role = Group.objects.get(id=role_id)

        user.groups.add(role)
        return Response(
            {"message": "Role assigned successfully"}, status=status.HTTP_200_OK
        )
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

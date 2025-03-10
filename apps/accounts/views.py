from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view

from apps.accounts.decorators import groups_required
from .models import CustomUser
from apps.companies.models import company, minerals, mineralsYear
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .serializers import (
    PermissionSerializer,
    RoleSerializer,
    TokenObtainPairSerializer,
    UserSerializer,
)


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)


class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # If the request reaches here, the token is valid
        return Response({"message": "Token is valid"}, status=200)


class UserDetailsView(APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)

            is_active = request.data.get("is_active")
            user_permission = request.data.get("user_permissions")

            if is_active is not None:
                if user.id == self.request.user.id:
                    return Response(
                        {"error": "You can't change state of your account"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                user.is_active = is_active

            if user_permission is not None:
                user_group = user.groups.first()

                if user_group:
                    if isinstance(user_permission, str):
                        user_permission = [user_permission]

                    user_permissions = Permission.objects.filter(
                        name__in=user_permission
                    )
                    user_group.permissions.set(user_permissions)
                    user_group.save()

                else:
                    return Response(
                        {"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                    )

            user.save()
            return Response(
                {"message": "User updated successfully"},
                status=status.HTTP_201_CREATED,
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            user = get_object_or_404(CustomUser, pk=pk)
            if user.id == self.request.user.id:
                return Response(
                    {"error": "You can't delete your own account"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            user.delete()
            return Response(
                {"message": "User deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["POST"])
def create_role(request):
    name = request.data.get("role")
    if not name:
        return Response(
            {"message": "Name field is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    Group.objects.create(name=name)
    return Response({"message": "Role created successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_permission(request):
    name = request.data.get("permission")
    codename = request.data.get("codename")
    model_name = request.data.get("modelname")
    model_map = {
        "companies": company,
        "mineral": minerals,
        "mineralYear": mineralsYear,
        "user": CustomUser,
    }

    model = model_map.get(model_name)
    if not all([name, codename, model_name]):
        return Response(
            {"error": "name, codename and model are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:

        contentType = ContentType.objects.get_for_model(model)
    except ContentType.DoesNotExist:
        return Response(
            {"error": f"Model '{model}' does not exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    Permission.objects.create(name=name, codename=codename, content_type=contentType)
    return Response(
        {"message": "Permission created successfully"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def assign_permission_to_role(request):
    permissionID = request.data.get("permission_id")
    roleID = request.data.get("role_id")

    if not all([permissionID, roleID]):
        return Response(
            {"error": "please provide role and permission"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        role = Group.objects.get(id=roleID)
    except Group.DoesNotExist:
        return Response(
            {"error": "Role does not exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        permission = Permission.objects.get(id=permissionID)
    except Permission.DoesNotExist:
        return Response(
            {"error": "Permission does not exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    role.permissions.add(permission)

    return Response(
        {"message": "Permission assigned successfully"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def assign_role(request):
    user_id = request.data.get("user_id")
    role_id = request.data.get("role_id")

    if not all([user_id, role_id]):
        return Response(
            {"error": "user id and role id are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = CustomUser.objects.get(id=user_id)
        role = Group.objects.get(id=role_id)

        user.groups.clear()
        user.groups.add(role)
        return Response(
            {"message": "Role assigned successfully"}, status=status.HTTP_200_OK
        )
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@groups_required("admin")
def list_user(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_roles(request):
    roles = Group.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_permission(response):
    permission = Permission.objects.all()
    serializer = PermissionSerializer(permission, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

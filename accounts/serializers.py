from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    groups = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "photo",
            "password",
            "groups",
            "permission",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_groups(self, user):
        return user.groups.values_list("name", flat=True)

    def get_permission(self, user):
        permissions = user.groups.values_list("permissions__name", flat=True).distinct()
        return list(permissions)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["groups"] = list(user.groups.values_list("name", flat=True))
        return data


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type"]

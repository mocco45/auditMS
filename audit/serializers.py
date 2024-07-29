from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, Role, mineralsYear, minerals, company
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
   
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            attrs["username"] = user.username  # Required for TokenObtainPairSerializer
            return super().validate(attrs)

        raise serializers.ValidationError({"detail": "Invalid credentials"})

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        slug_field='codename',
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']

# class CustomUserSerializer(serializers.ModelSerializer):
#     role = RoleSerializer()

#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'role', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         role_data = validated_data.pop('role')
#         role, created = Role.objects.get_or_create(**role_data)
#         user = CustomUser.objects.create_user(role=role, **validated_data)
#         return user
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type', 'codename']

class PermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class MineralYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = mineralsYear
        fields = '__all__'
        
class MineralSerializer(serializers.ModelSerializer):
    class Meta:
        model = minerals
        fields = '__all__'
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'
        

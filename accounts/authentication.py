from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Ensure request.COOKIES is accessed correctly
        token = request.COOKIES.get("access_token")
        if not token:  # If the token is None or empty
            return None

        try:
            # Validate the token using SimpleJWT's method
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception as e:
            # Handle any validation errors
            return None

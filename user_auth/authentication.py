from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Overrides the default authenticate method to allow token retrieval from cookies if the Authorization header is not present.
        This allows the frontend to store the access token in an HttpOnly cookie and still have it work with JWT authentication.
        """

        public_paths = ['/api/login/', '/api/register/', '/api/logout/', '/api/password_reset/']
        public_prefixes = ['/api/activate/', '/api/password_confirm/']
        
        if request.path in public_paths or any(request.path.startswith(prefix) for prefix in public_prefixes):
            return None
        

        header = self.get_header(request)
        
        if header is None:
            raw_token = request.COOKIES.get('access_token') or None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
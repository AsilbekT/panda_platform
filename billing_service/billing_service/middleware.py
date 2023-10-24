# middleware.py

from django.http import JsonResponse
import requests
import jwt


class SimpleUser:
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.username = user_data.get('username')
        self.is_active = True 


class GetUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        if token:
            try:
                # Decode JWT token
                
                # Prepare headers with the Bearer token that came in the original request
                headers = {'Authorization': f'Bearer {token}'}
                
                # Fetch user from User service
                response = requests.get("https://userservice.inminternational.uz/users", headers=headers)
                
                if response.status_code == 200:
                    user_json = response.json()
                    request.user = SimpleUser(user_json.get('data', {}))  # Use SimpleUser object

            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass


        # Continue processing the request
        response = self.get_response(request)
        return response


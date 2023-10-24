from functools import wraps
from django.http import JsonResponse
import requests

def verify_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        if not token:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        verify_token_url = "https://authservice.inminternational.uz/auth/verify-token"
        headers = {'Authorization': f'Bearer {token}'}

        try:
            response = requests.get(verify_token_url, headers=headers)
            print(response.json())
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.RequestException as e:
            # Log the exception for debugging
            print(f"An error occurred while verifying token: {e}")
            return JsonResponse({"message": "Internal Server Error"}, status=500)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == 'success':
                request.username = response_data.get('data', {}).get('username')
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "Invalid Token or Token not provided"}, status=401)

    return _wrapped_view

import requests
from rest_framework import viewsets, status
from .utils import standardResponse
from .models import Episode, UserSubscription


class BaseViewSet(viewsets.ModelViewSet):
    def validate_token(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return False

        token = auth_header[1]
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(
            'https://authservice.inminternational.uz/auth/verify-token', headers=headers)

        # For debugging purposes; remove or comment out in production
        return response.status_code == 200, response.json()['data'], token

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return standardResponse(status="success", message="Items retrieved", data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return standardResponse(status="success", message="Item created", data=serializer.data)
        return standardResponse(status="error", message="Invalid data", data=serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        # Fetch the authorization header
        auth_header = request.headers.get('Authorization', '')

        # Determine if the content is free
        if isinstance(instance, Episode):
            # Accessing the series attributes from the episode
            is_free_content = instance.series.is_free
        else:
            is_free_content = instance.is_free

        # If no auth header is provided or the content is free, serve the content as it is
        if is_free_content:
            return standardResponse(status="success", message="Item retrieved", data=serialized_data)

        # If an auth header is provided, validate the token
        if auth_header.startswith('Bearer '):
            auth_status, user_info, _ = self.validate_token(request)

            # If the token is valid, check the user's subscription
            if auth_status and self.user_has_access_to_content(user_info['username'], instance):
                return standardResponse(status="success", message="Item retrieved", data=serialized_data)

        # For unauthenticated users or users without a valid subscription, hide the main content URL
        if isinstance(instance, Episode):
            serialized_data['episode_content_url'] = None
        else:
            serialized_data['main_content_url'] = None
        return standardResponse(status="success", message="Item retrieved", data=serialized_data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return standardResponse(status="success", message="Item updated", data=serializer.data)
        return standardResponse(status="error", message="Invalid data", data=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return standardResponse(status="success", message="Item deleted")

    def user_has_access_to_content(self, username, content):
        try:
            user_subs = UserSubscription.objects.get(username=username)

            # Check if the subscription is active
            if not user_subs.is_active:
                return False

            # If the content is an episode, then get its parent series
            if isinstance(content, Episode):
                content_to_check = content.series
            else:
                content_to_check = content

            # Check if the content (movie/series) is available under the user's subscription plan
            if content_to_check.available_under_plans.filter(name=user_subs.subscription_plan_name).exists():
                return True

            return False
        except UserSubscription.DoesNotExist:
            return False

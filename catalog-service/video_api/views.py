from django.http import JsonResponse
from django.views import View
import requests
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views import View
from django.conf import settings
import os

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadView(View):
    def validate_token(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return False

        token = auth_header[1]
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(
            'https://authservice.inminternational.uz/auth/verify-token', headers=headers)

        # For debugging purposes; remove or comment out in production
        return response.status_code == 200

    def post(self, request, *args, **kwargs):
        if not self.validate_token(request):
            return JsonResponse({'status': 'failed', 'message': 'Invalid token or no token provided.'})

        video = request.FILES.get('video')
        content_id = request.POST['content_id']
        if video:
            # Define a custom directory path relative to MEDIA_ROOT
            custom_directory_path = os.path.join(
                settings.MEDIA_ROOT, 'custom_videos')

            # Create the directory if it doesn't exist
            if not os.path.exists(custom_directory_path):
                os.makedirs(custom_directory_path)

            # Save the video using FileSystemStorage
            fs = FileSystemStorage(location=custom_directory_path)
            filename = fs.save(video.name, video)

            # Generate the URL to access the video
            full_file_path = os.path.join(fs.location, filename)
            print(full_file_path)
            data = {'status': 'success', 'message': 'Video uploaded',
                    'video_url': full_file_path, "content_id": content_id}
            response = requests.post(
                "http://127.0.0.1:8000/convert", json=data)
            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': 'Video uploaded and conversion initiated', 'video_url': full_file_path})
            else:
                return JsonResponse({'status': 'failed', 'message': f'Video uploaded but conversion failed. Response: {response.text}'})

        return JsonResponse({'status': 'failed', 'message': 'No video uploaded'})

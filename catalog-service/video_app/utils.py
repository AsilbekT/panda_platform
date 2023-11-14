import requests
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .models import SubscriptionPlan


BILLING_SERVICE_URL = "http://127.0.0.1:8001/"


def standardResponse(status, message, data, pagination=None):
    response = {
        'status': status,
        'message': message,
        'data': data
    }
    if pagination:
        response['pagination'] = pagination
    return Response(response)


def paginate_queryset(queryset, request):
    page_number = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('size', 10))

    paginator = Paginator(queryset, page_size)
    try:
        paginated_queryset = paginator.page(page_number)
    except EmptyPage:
        return [], standardResponse(status="error", message="Invalid page number.", data={})
    except PageNotAnInteger:
        return [], standardResponse(status="error", message="Page number is not an integer.", data={})

    pagination_data = {
        'total': paginator.count,
        'page_size': page_size,
        'current_page': page_number,
        'total_pages': paginator.num_pages,
        'next': paginated_queryset.has_next(),
        'previous': paginated_queryset.has_previous(),
    }

    return paginated_queryset, pagination_data


def validate_file_size(value):
    filesize = value.size

    if filesize > 2048000:
        raise ValidationError(
            "The maximum file size that can be uploaded is 2 MB")
    else:
        return value


def validate_image_file(value):
    try:
        image = Image.open(value)
        image.verify()
    except:
        raise ValidationError("Invalid image format")


def user_has_active_plan(username, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(BILLING_SERVICE_URL +
                            f'billing/{username}/subscriptions/', headers=headers)

    if response.status_code == 200:
        return True
    return False

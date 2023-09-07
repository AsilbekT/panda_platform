from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from PIL import Image


def standardResponse(status, message, data=None):
    return Response({
        "status": status,
        "message": message,
        "data": data
    })


def paginate_queryset(queryset, request):
    page_number = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('size', 10))

    paginator = Paginator(queryset, page_size)
    try:
        paginated_queryset = paginator.page(page_number)
    except Exception:
        return None, standardResponse(status="error", message="Invalid page.", data={})

    return paginated_queryset, None


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

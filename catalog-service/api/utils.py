from rest_framework.response import Response
from django.core.paginator import Paginator

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
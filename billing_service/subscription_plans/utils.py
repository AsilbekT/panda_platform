import requests

BASE_URL = 'http://127.0.0.1:8001/plans/'

def send_request_to_catalog_service(instance, method):
    """
    Helper function to send HTTP requests to the catalog service.
    """
    url = f"{BASE_URL}{instance.id}/" if method in ['PUT', 'DELETE'] else BASE_URL

    data = {
        'name': instance.name,
        'price': str(instance.price),
        'duration_days': instance.duration_days,
    }

    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request(method, url, json=data, headers=headers)
    print(response.json())

    if response.status_code in [200, 201]:  # 200 for OK, 201 for CREATED
        print(f'{method} request sent successfully')
    else:
        print(f'{method} request failed with status code {response.status_code}')

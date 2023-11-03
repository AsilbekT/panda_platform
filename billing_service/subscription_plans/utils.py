import uuid
import requests
import hashlib

BASE_URL = 'http://127.0.0.1:8000/plans/'
CATALOG_SERVICE_SUBSCRIPTION_URL = 'http://127.0.0.1:8000/subscriptions/'

CLICK_SECRET_KEY = 'DKmiRNDgKgtxf5'
MERCHANT_SERVICE_ID = '30124'
MERCHANT_USER_ID = '36027'


def create_click_payment_url(user_id, plan_id, price):
    # Generate a unique transaction ID for the payment

    # Assuming you have a model to store the transaction with a foreign key to the user
    # PaymentTransaction.objects.create(user_id=user_id, transaction_id=str(transaction_id), amount=price)

    # Construct the payment URL
    payment_url = f"https://my.click.uz/services/pay?service_id={MERCHANT_SERVICE_ID}&merchant_id={MERCHANT_USER_ID}&amount={price}&transaction_param="
    return payment_url


def verify_click_signature(request, merchant_prepare_id):
    # Extract the necessary parameters from the request
    click_trans_id = request.POST.get('click_trans_id')
    service_id = request.POST.get('service_id')
    click_paydoc_id = request.POST.get('click_paydoc_id')
    merchant_trans_id = request.POST.get('merchant_trans_id')
    amount = request.POST.get('amount')
    action = request.POST.get('action')
    sign_time = request.POST.get('sign_time')
    sign_string = request.POST.get('sign_string')

    # Create the sign string
    raw_sign_string = f"{click_trans_id}{service_id}{CLICK_SECRET_KEY}{merchant_trans_id}{merchant_prepare_id}{click_paydoc_id}{amount}{action}{sign_time}"
    generated_sign_string = hashlib.md5(
        raw_sign_string.encode('utf-8')).hexdigest()

    # Compare the generated sign string with the one from the request
    return generated_sign_string == sign_string


def send_request_to_catalog_service(instance, method):
    """
    Helper function to send HTTP requests to the catalog service.
    """
    url = f"{BASE_URL}{instance.id}/" if method in [
        'PUT', 'DELETE'] else BASE_URL

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


def generate_merchant_prepare_id():
    return uuid.uuid4().hex


def generate_merchant_confirm_id():
    return uuid.uuid4().hex


def send_user_subscription_to_catalog(instance):
    """
    Sends the UserSubscription data to the catalog service.
    """
    # Extract the necessary data from the instance
    data = {
        'user_id': instance.billing_info.user_id,
        'username': instance.billing_info.username,
        'subscription_plan_name': instance.subscription_plan.name,
        'start_date': instance.start_date.isoformat(),
        'end_date': instance.end_date.isoformat(),
        'status': instance.status
    }

    # Send the data to the catalog service
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(
        CATALOG_SERVICE_SUBSCRIPTION_URL, json=data, headers=headers)

    # Check the response
    if response.status_code in [200, 201]:  # 200 for OK, 201 for CREATED
        print(
            f'UserSubscription data sent successfully for user {instance.billing_info.username}')
    else:
        print(
            f'Failed to send UserSubscription data for user {instance.billing_info.username}. Status code: {response.status_code}')

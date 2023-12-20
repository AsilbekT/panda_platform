class PaymentUtil:
    def __init__(self) -> None:
        self.key = None

    @staticmethod
    def charge_user(user_id, amount, currency='USD'):
        print(f"Charged user {user_id} {amount} {currency}")
        return True

    @staticmethod
    def refund_user(user_id, amount, currency='USD'):
        print(f"Refunded user {user_id} {amount} {currency}")
        return True

from decimal import Decimal


class Settlement:
    def __init__(self):
        self.customer: str = None
        self.account: str = None
        self.number: str = None
        self.value: Decimal = 0.0
        self.value_to_pay: Decimal = 0.0
        self.date: str = None
        self.due_date: str = None
        self.external_id: str = None

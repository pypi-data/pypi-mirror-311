from decimal import Decimal
from typing import List, Optional
from datetime import datetime


class CustomerTask:
    def __init__(self):
        self.external_id: str = None
        self.name: str = None
        self.date_start: Optional[datetime] = None
        self.date_end: Optional[datetime] = None
        self.goals: List[CustomerTaskGoal] = []
        self.customers: List[TaskCustomers] = []


class CustomerTaskGoal:
    def __init__(self):
        self.product_external_id: str = None
        self.type: str = None
        self.goal_value: Decimal = 0.0


class TaskCustomers:
    def __init__(self):
        self.customer_external_id: str = None

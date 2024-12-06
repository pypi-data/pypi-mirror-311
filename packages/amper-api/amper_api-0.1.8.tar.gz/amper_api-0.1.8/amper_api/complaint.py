from datetime import datetime
from typing import List, Optional

from amper_api.customer import Customer


class Complaint:
    def __init__(self):
        self.id: int = 0
        self.lines: List[ComplaintLine] = []
        self.attachments = []
        self.notes = []
        self.nr: str = None
        self.note: str = None
        self.status: str = None
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.updated_by: Optional[Customer] = None
        self.created_by: Optional[Customer] = None
        self.customer_external_id: str = None
        self.customer: Optional[Customer] = None


class ComplaintLine:
    def __init__(self):
        self.id: int = 0
        self.product_id: int = 0
        self.name: str = None
        self.purchase_date: str = None
        self.order: str = None
        self.description: str = None
        self.complaint: int = 0
        self.product_external_id: str = None

from typing import List

from amper_api.customer import Customer
from amper_api.settlement import Settlement


class CashDocumentOperation:
    def __init__(self):
        self.id: int = None
        self.settlement: Settlement = None
        self.settlement_external_id: str = None
        self.amount: str = None
        self.settlement_number: str = None
        self.type: str = None
        self.document_header: int = None


class CashDocument:
    def __init__(self):
        self.id: int = None
        self.cash_document_operations: List[CashDocumentOperation] = None
        self.customer_external_id: str = None
        self.customer: Customer = None
        self.number: str = None
        self.created_at: str = None
        self.status: str = None
        self.type: str = None
        self.date_of_exportation = None
        self.amount: str = None
        self.user: str = None
        self.description: str = None
        self.is_system_operation: bool = False
        self.ordinal: str = None
        self.cash_drawer: int = None
        self.sales_rep_email: str = None
        self.sales_rep_first_name: str = None
        self.sales_rep_last_name: str = None
        self.sales_rep_phone: str = None
        self.sales_rep_identifier: str = None

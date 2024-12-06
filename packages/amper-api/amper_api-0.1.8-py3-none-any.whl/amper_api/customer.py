from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from amper_api.product import PriceLevel


class Account:
    def __init__(self):
        self.name: str = None
        self.short_name: str = None
        self.external_id: str = None
        self.city: str = ''
        self.postal_code: str = ''
        self.street: str = ''
        self.email: str = None
        self.phone: str = None
        self.voivodeship: str = None
        self.tax_id: str = None
        self.customers: List[Customer] = []


class Customer:
    def __init__(self):
        self.external_id: str = None
        self.name: str = None
        self.friendly_name: str = None
        self.short_name: str = None
        self.primary_email: str = None
        self.phone: str = None
        self.city: str = ''
        self.postal_code: str = ''
        self.street: str = ''
        self.tax_id: str = None
        self.comments: str = None
        self.price_level_external_id: str = None
        self.complementary_price_level_external_id: str = None
        self.payment_form_external_id: str = None
        self.login: str = None
        self.password: str = None
        self.trade_credit_limit: Decimal = 0.0
        self.overdue_limit: Decimal = 0.0
        self.discount: Decimal = 0.0
        self.currency_code: str = None
        self.id: int = 0
        self.overdue_settlements: int = 0
        self.max_num_of_overdue_settlements: int = 0
        self.currency_format: str = None
        self.ftp_host: str = None
        self.ftp_port: str = None
        self.ftp_user: str = None
        self.ftp_pass: str = None
        self.ftp_secure: bool = False
        self.type: str = None
        self.added_at: datetime = datetime.now()
        self.updated_at: Optional[datetime] = None
        self.first_login_at: Optional[datetime] = None
        self.is_free_shipping: bool = False
        self.account: Optional[int] = None
        self.default_address: str = None
        self.currency: str = None
        self.updatable_fields: str = None
        self.stock_location_external_id: str = None
        self.concession_a_valid_until: Optional[datetime] = None
        self.concession_b_valid_until: Optional[datetime] = None
        self.concession_c_valid_until: Optional[datetime] = None
        self.default_sales_rep_identifier: str = None
        self.check_minimal_price: bool = False
        self.is_locked_for_sale: bool = False
        self.ean: str = None
        self.latitude: Optional[Decimal] = None
        self.longitude: Optional[Decimal] = None
        self.export_customer: bool = False
        self.value_restrictions: Optional[Decimal] = None
        self.value_restrictions_limit: Optional[Decimal] = None
        self.weight_restrictions: Optional[Decimal] = None
        self.weight_restrictions_limit: Optional[Decimal] = None
        self.free_shipping_from: Optional[Decimal] = None


class CustomerProductLogisticMinimum:
    def __init__(self):
        self.external_id: str = None
        self.product_external_id: str = None
        self.customer_external_id: str = None
        self.logistic_minimum: Decimal = 0


class Address:
    def __init__(self):
        self.name: str = None
        self.city: str = None
        self.postal_code: str = None
        self.street: str = None
        self.street_continuation: str = None
        self.email: str = None
        self.phone: str = None
        self.voivodeship: str = None
        self.external_id: str = None
        self.customer_external_id: str = None
        self.updatable_fields: str = None


class CustomerCategory:
    def __init__(self):
        self.external_id: str = None
        self.parent_external_id: str = None
        self.name: str = None
        self.description: str = None
        self.seo_tags: str = None
        self.order: str = None
        self.updatable_fields: str = None


class CustomerCategoryRelation:
    def __init__(self):
        self.external_id: str = None
        self.category_external_id: str = None
        self.customer_external_id: str = None


class CustomerSalesRepresentative:
    def __init__(self):
        self.external_id: str = None
        self.sales_representative_identifier: str = None
        self.customer_category_external_id: str = None
        self.customer_external_id: str = None


class PaymentForm:
    def __init__(self):
        self.external_id: str = None
        self.name: str = None
        self.is_cash: bool = False
        self.default_payment_date_in_days: int = 14


class CustomerForExport:
    def __init__(self):
        self.external_id: str = None
        self.name: str = None
        self.short_name: str = None
        self.primary_email: str = None
        self.phone: str = None
        self.city: str = ''
        self.postal_code: str = ''
        self.street: str = ''
        self.tax_id: str = None
        self.comments: str = None
        self.price_level_external_id: str = None
        self.payment_form_external_id: str = None
        self.login: str = None
        self.password: str = None
        self.trade_credit_limit: Decimal = 0.0
        self.overdue_limit: Decimal = 0.0
        self.discount: Decimal = 0.0
        self.currency_code: str = None
        self.id: int = 0
        self.overdue_settlements: int = 0
        self.currency_format: str = None
        self.ftp_host: str = None
        self.ftp_port: str = None
        self.ftp_user: str = None
        self.ftp_pass: str = None
        self.ftp_secure: bool = False
        self.type: str = None
        self.added_at: datetime = datetime.now()
        self.updated_at: Optional[datetime] = None
        self.first_login_at: Optional[datetime] = None
        self.is_free_shipping: bool = False
        self.currency: str = None
        self.updatable_fields: str = None
        self.stock_location_external_id: str = None
        self.concession_a_valid_until: Optional[datetime] = None
        self.concession_b_valid_until: Optional[datetime] = None
        self.concession_c_valid_until: Optional[datetime] = None
        self.default_sales_rep_identifier: str = None
        self.account: int = None
        self.default_price: PriceLevel = None
        self.payment_form: PaymentForm = None
        self.default_sales_rep: SalesRepresetnative = None
        self.default_stock_location = None
        self.default_address: Address = None


class SalesRepresetnative:
    def __init__(self):
        self.id: int = 0
        self.deleted = None
        self.identifier: str = None
        self.first_name: str = None
        self.last_name: str = None
        self.phone: str = None
        self.email: str = None
        self.status: str = None
        self.keycloak_id: str = None
        self.supervisor: str = None


class CustomerNote:
    def __init__(self):
        self.id: int = 0
        self.author: str = None
        self.customer: int = 0
        self.body: str = None
        self.note_type: CustomerNoteType = None
        self.added_at: datetime = None
        self.created_by: str = None


class CustomerNoteType:
    def __init__(self):
        self.id: int = 0
        self.type: str = None
        self.value: str = None
        self.order: int = 0

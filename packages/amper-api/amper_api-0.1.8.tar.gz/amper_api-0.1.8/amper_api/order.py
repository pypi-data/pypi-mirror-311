from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from amper_api.promotion import Promotion
from amper_api.customer import Customer


class OrderList:
    def __init__(self):
        self.token: str = None
        self.created: datetime = None
        self.status: str = None
        self.user_email: str = None
        self.total_gross: str = None


class OrderLine:
    def __init__(self):
        self.id: int = None
        self.attributesList = []
        self.product_external_id: str = None
        self.product_short_code: str = None
        self.external_id: str = None
        self.product_name: str = None
        self.product_sku: str = None
        self.quantity: Decimal = 0.0
        self.base_price_net: str = None
        self.discount: str = None
        self.unit_price_net: str = None
        self.unit_price_gross: str = None
        self.tax_rate: str = None
        self.is_promotion_reward: bool = False
        self.product: int = None
        self.promotion_condition: Optional[int] = None
        self.promotion: Optional[Promotion] = None


class ShippingAddress:
    def __init__(self):
        self.external_id: str = None
        self.id: int = None
        self.deleted = None
        self.name: str = None
        self.city: str = None
        self.postal_code: str = None
        self.street: str = None
        self.street_continuation: str = None
        self.email: str = None
        self.phone = None
        self.voivodeship: str = None
        self.customer: int = None


class Order:
    def __init__(self):
        self.id: Optional[int] = None
        self.external_id: str = None
        self.token: str = None
        self.lines: List[OrderLine] = []
        self.customer_external_id: str = None
        self.shipping_address: ShippingAddress = None
        self.billing_address: ShippingAddress = None
        self.customer: Customer = None
        self.created: datetime = None
        self.updated: datetime = None
        self.status: str = None
        self.user_email: str = None
        self.shipping_price_net: str = None
        self.shipping_price_gross: str = None
        self.products_total_net: str = None
        self.products_total_gross: str = None
        self.total_net: str = None
        self.total_gross: str = None
        self.paid: Decimal = 0.0
        self.discount_amount: Decimal = 0.0
        self.customer_note: str = None
        self.shipment_type: Optional[int] = None
        self.order_number: str = None
        self.order_type: str = None
        self.form_of_payment: str = None

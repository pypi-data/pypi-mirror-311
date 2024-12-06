from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from amper_api.customer import Customer


class Document:
    def __init__(self):
        self.external_id: str = None
        self.id: int = None
        self.document_lines: List[DocumentLine] = []
        self.customer_external_id: str = None
        self.customer: Customer = None
        self.document_provider: Optional[DocumentProvider] = None
        self.visit: Visit = None
        self.document_type: DocumentType = None
        self.stock_location = None
        self.number: str = None
        self.status: str = None
        self.date: datetime = None
        self.due_date: Optional[datetime] = None
        self.description: str = None
        self.value_net: Decimal = 0.0
        self.value_gross: Decimal = 0.0
        self.created_at: Optional[datetime] = None
        self.modified_at: Optional[datetime] = None
        self.ordinal: str = None
        self.source_document: int = None
        self.print_date: Optional[datetime] = None
        self.synchronization_date: Optional[datetime] = None
        self.delivery_date: Optional[datetime] = None
        self.percentage_discount: Decimal = 0.0
        self.username: str = None
        self.document_provider_short_name: str = None
        self.document_type_name: str = None
        self.payment_form_external_id: str = None
        self.is_external_document: str = None
        self.sales_rep_identifier: str = None
        self.sales_rep_first_name: str = None
        self.sales_rep_last_name: str = None
        self.sales_rep_email: str = None
        self.sales_rep_phone: str = None
        self.document_metadata = None
        self.coords_details: CoordsDetails = None


class DocumentLine:
    def __init__(self):
        self.id: int = None
        self.external_id: str = None
        self.document: str = None
        self.product_symbol: str = None
        self.product_ean: str = None
        self.product_additional_fees_net: Decimal = 0.0
        self.product_additional_fees_gross: Decimal = 0.0
        self.product_name: str = None
        self.vat: int = None
        self.unit: str = None
        self.quantity: Decimal = 0.0
        self.unit_aggregate: str = None
        self.quantity_aggregate: Decimal = 0.0
        self.price_net: Decimal = 0.0
        self.price_gross: Decimal = 0.0
        self.value_net: Decimal = 0.0
        self.value_gross: Decimal = 0.0
        self.manufacturer: str = None
        self.make: str = None
        self.group: str = None
        self.product_external_id: str = None
        self.product_vat: int = None
        self.base_price: Decimal = 0.0
        self.percentage_discount: Decimal = 0.0
        self.source_document_line: int = None
        self.source_price_level_desc = None
        self.created_at: Optional[datetime] = None
        self.modified_at: Optional[datetime] = None
        self.document_promotion: str = None
        self.promotion_condition: str = None
        self.promotion_condition_relation: str = None
        self.source_price_level: Optional[int] = None
        self.price_level_external_id: str = None
        self.line_metadata: List[LineMetadata] = []
        self.applied_promotion: AppliedPromotion = None
        self.is_promotion_reward: bool = False
        self.piggy_bank_budget: Optional[int] = None
        self.piggy_bank_budget_built: Optional[int] = None
        self.user_discount: Optional[Decimal] = None
        self.product: int = None
        self.budget: Optional[int] = None
        self.source_target_goal: Optional[int] = None
        self.export_rewards_to_a_separate_doc: bool = False


class DocumentType:
    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.series: str = None
        self.template: str = None
        self.annual: bool = False
        self.monthly: bool = False
        self.current_number: int = None
        self.model_name: str = None


class Visit:
    def __init__(self):
        self.id: int = None
        self.customer_name: str = None
        self.customer_short_name: str = None
        self.sales_representatives: str = None
        self.date_start: Optional[datetime] = None
        self.date_end: Optional[datetime] = None
        self.username: str = None
        self.virtual_visit: bool = False
        self.coords_details: CoordsDetails = None
        self.customer: int = None


class AppliedPromotion:
    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.short_code: str = None
        self.external_id = None
        self.start: datetime = None
        self.end: datetime = None
        self.priority: int = None
        self.description: str = None
        self.internal_description: str = None
        self.external_identifier: str = None
        self.is_required: bool = False


class DocumentProvider:
    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.short_name: str = None


class Coords:
    def __init__(self):
        self.speed: str = None
        self.heading: str = None
        self.accuracy: str = None
        self.altitude: str = None
        self.latitude: str = None
        self.longitude: str = None
        self.altitudeAccuracy: str = None

class CoordsDetails:
    def __init__(self):
        self.coords: Coords = None
        self.timestamp: str = None


class LineMetadata:
    def __init__(self):
        self.step: int = None
        self.amount: Optional[Decimal] = None
        self.discount: Optional[Decimal] = None
        self.description: str = None
        self.relation_id: Optional[int] = None
        self.condition_id: Optional[int] = None
        self.price_level_id: Optional[int] = None

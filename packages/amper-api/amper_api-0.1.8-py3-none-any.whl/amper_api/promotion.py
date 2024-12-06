from decimal import Decimal
from typing import List, Optional
from datetime import datetime


class Promotion:
    def __init__(self):
        self.id: Optional[int] = None
        self.external_id: str = None
        self.name: str = None
        self.start: Optional[datetime] = None
        self.end: Optional[datetime] = None
        self.priority: Optional[int] = None
        self.description: str = None
        self.short_code: str = None
        self.is_enabled: Optional[bool] = None
        self.updatable_fields: str = None
        self.external_identifier: str = None
        self.internal_description: str = None
        self.replace_gratifications: str = None


class PromotionCustomer:
    def __init__(self):
        self.external_id: str = None
        self.promotion_external_id: str = None
        self.customer_external_id: str = None


class PromotionCustomerCategory:
    def __init__(self):
        self.external_id: str = None
        self.promotion_external_id: str = None
        self.customer_category_external_id: str = None


class ConditionRelation:
    def __init__(self):
        self.external_id: str = None
        self.parent_relation_external_id: str = None
        self.promotion_external_id: str = None
        self.relation: str = None
        self.order: Optional[int] = None
        self.multiply_reward: Optional[int] = None


class ConditionRelationPromotionCondition:
    def __init__(self):
        self.external_id: str = None
        self.condition_relation_external_id: str = None
        self.promotion_condition_external_id: str = None
        self.order: Optional[int] = None


class PromotionCondition:
    def __init__(self):
        self.external_id: str = None
        self.name: str = None


class PromotionConditionItem:
    def __init__(self):
        self.external_id: str = None
        self.promotion_condition_external_id: str = None
        self.product_external_id: str = None
        self.product_category_external_id: str = None
        self.value: Decimal = 0.0
        self.value_type: str = None
        self.value_max: Decimal = 0.0
        self.create_temporary_category: bool = False
        self.temporary_category_name: str = None
        self.temporary_category_products: List[str] = []


class PromotionRewards:
    def __init__(self):
        self.external_id: str = None
        self.promotion_external_id: str = None
        self.condition_relation_external_id: str = None
        self.product_external_id: str = None
        self.product_category_external_id: str = None
        self.quantity: Decimal = 0.0
        self.price: Decimal = 0.0
        self.value_type: str = None
        self.reward_value: Decimal = 0.0
        self.reward: str = None

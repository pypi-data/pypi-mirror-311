from typing import Optional
from datetime import datetime


class SchedulerEntry:
    def __init__(self):
        self.external_id: str = None
        self.name: str = None
        self.customer_external_id: str = None
        self.cron_expression: str = None
        self.related_user_login: str = None
        self.sales_representative_identifier: str = None
        self.is_enabled: bool = False
        self.updatable_fields: str = None
        self.entry_date: datetime = None
        self.ended_at: Optional[datetime] = None
        self.ex_dates: Optional[datetime] = None

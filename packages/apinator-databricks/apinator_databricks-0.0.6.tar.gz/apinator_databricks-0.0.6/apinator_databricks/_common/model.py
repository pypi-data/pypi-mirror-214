from datetime import datetime

from apinator.common import StrictBaseModel


class DatabricksBase(StrictBaseModel):
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

class SecurableDatabricksBase(DatabricksBase):
    securable_type: str
    securable_kind: str
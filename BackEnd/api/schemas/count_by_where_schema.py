from pydantic import BaseModel
from typing import Any, Optional

class CountByWhereGLB(BaseModel):
    column_name: Optional[str] = None
    table_or_view_name: Optional[str]
    where_conditions: Optional[str] = None

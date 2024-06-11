from pydantic import BaseModel
from typing import Any, Optional

class GetAllByWhereGLB(BaseModel):
    sort_column: Optional[str] = None
    limit_index: Optional[int]
    limit_range: Any
    table_or_view_name: Optional[str]
    where_conditions: Optional[str] = None

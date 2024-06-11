from typing import Optional, List
from pydantic import BaseModel

class Search(BaseModel):
    value: Optional[str]
    search_by: Optional[str]
    fromdate: Optional[str]
    todate: Optional[str]
    regex: Optional[bool]

class Column(BaseModel):
    data: Optional[str]
    name: Optional[str]
    searchable: Optional[bool]
    orderable: Optional[bool]
    search: Optional[Search]

class Order(BaseModel):
    column: Optional[str]  # Assume this references the name of a Column
    order_by: Optional[str]  # 'asc' or 'desc'

class DatatableGLB(BaseModel):
    columns: Optional[List[Column]]
    orders: Optional[List[Order]]
    start: int
    length: str
    search: Optional[Search]
    searches: Optional[List[Search]]


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.policy_model import Policy
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.policy_schema import PolicyCreate, PolicyUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_policy_view_model import GetPoliciesView
import json

router = APIRouter()

@router.get("/get-policies")
async def get_policies_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Policy)
    policies = await repo.get_all()
    if not policies:
        raise HTTPException(status_code=404, detail="Policies not found")
    return policies

@router.get("/get-policy-by-id")
async def get_policy_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Policy)
    policy = await repo.get_by_field(policy_id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@router.post("/create-policy", status_code=201)
async def create_policy_endpoint(policy_data: PolicyCreate, db: AsyncSession = Depends(get_session)):
    new_policy = Policy(**policy_data.dict())
    repo = GenericRepository(db, Policy)
    new_policy = await repo.insert(new_policy)
    return new_policy

@router.put("/update-policy")
async def update_policy_endpoint(id: int, policy_data: PolicyUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Policy)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = policy_data.dict(exclude_unset=True)

    updated_policy = await repo.update('policy_id', id, **update_data)
    if not updated_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return updated_policy

@router.delete("/delete-policy")
async def delete_policy_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Policy)
    success = await repo.delete('policy_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"message": "Policy deleted successfully"}

@router.get("/get-policies-view")
async def get_policies_view_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetPoliciesView)
    policies_view = await repo.get_all()
    if not policies_view:
        raise HTTPException(status_code=404, detail="Policies view not found")
    return policies_view

@router.get("/get-policy-grid-by-id")
async def get_policy_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetPoliciesView)
    policy = await repo.get_by_field(policy_id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@router.post("/get-policy-grid")
async def get_policy_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "policy_id DESC"  # Default sort
    if table_obj.orders and len(table_obj.orders) > 0:
        sort_information = f"{table_obj.orders[0].column} {table_obj.orders[0].order_by}"

    # Build where condition
    where_conditions = []
    for search in table_obj.searches or []:
        if search.search_by == "InsertDate" and search.fromdate and search.todate:
            where_conditions.append(f"(InsertDate BETWEEN '{search.fromdate}' AND '{search.todate}')")
        elif search.value:
            where_conditions.append(f"{search.search_by} LIKE '%{search.value}%'")

    where_clause = " AND ".join(where_conditions)
    where_clause = f" {where_clause}" if where_conditions else ""

    print("where condition: ", where_clause, where_conditions)

    dataGrid = GetAllByWhereGLB()
    dataGrid.table_or_view_name = "GetPoliciesView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetPoliciesView)
    data = await repo.get_all_by_where(dataGrid)

    formatDataSource = []
    for policy in data:
        policy_dict = dict(policy)
        formatDataSource.append(policy_dict)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetPoliciesView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "policy_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": formatDataSource}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.payment_gateway_model import PaymentGateway
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.payment_gateway_schema import PaymentGatewayCreate, PaymentGatewayUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_payment_gateway_view_model import GetPaymentGatewaysView
import json

router = APIRouter()

@router.get("/get-payment-gateways")
async def get_payment_gateways_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PaymentGateway)
    payment_gateways = await repo.get_all()
    if not payment_gateways:
        raise HTTPException(status_code=404, detail="Payment gateways not found")
    return payment_gateways

@router.get("/get-payment-gateway-by-id")
async def get_payment_gateway_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PaymentGateway)
    payment_gateway = await repo.get_by_field(gateway_id=id)
    if not payment_gateway:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    return payment_gateway

@router.post("/create-payment-gateway", status_code=201)
async def create_payment_gateway_endpoint(payment_gateway_data: PaymentGatewayCreate, db: AsyncSession = Depends(get_session)):
    new_payment_gateway = PaymentGateway(**payment_gateway_data.dict())
    repo = GenericRepository(db, PaymentGateway)
    new_payment_gateway = await repo.insert(new_payment_gateway)
    return new_payment_gateway

@router.put("/update-payment-gateway")
async def update_payment_gateway_endpoint(id: int, payment_gateway_data: PaymentGatewayUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PaymentGateway)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = payment_gateway_data.dict(exclude_unset=True)

    updated_payment_gateway = await repo.update('gateway_id', id, **update_data)
    if not updated_payment_gateway:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    return updated_payment_gateway

@router.delete("/delete-payment-gateway")
async def delete_payment_gateway_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PaymentGateway)
    success = await repo.delete('gateway_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    return {"message": "Payment gateway deleted successfully"}

@router.get("/get-payment-gateways-view")
async def get_payment_gateways_view_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetPaymentGatewaysView)
    payment_gateways_view = await repo.get_all()
    if not payment_gateways_view:
        raise HTTPException(status_code=404, detail="Payment gateways view not found")
    return payment_gateways_view

@router.get("/get-payment-gateway-grid-by-id")
async def get_payment_gateway_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetPaymentGatewaysView)
    payment_gateway = await repo.get_by_field(gateway_id=id)
    if not payment_gateway:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    return payment_gateway

@router.post("/get-payment-gateway-grid")
async def get_payment_gateway_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "gateway_id DESC"  # Default sort
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
    dataGrid.table_or_view_name = "GetPaymentGatewaysView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetPaymentGatewaysView)
    data = await repo.get_all_by_where(dataGrid)

    formatDataSource = []
    for payment_gateway in data:
        payment_gateway_dict = dict(payment_gateway)
        formatDataSource.append(payment_gateway_dict)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetPaymentGatewaysView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "gateway_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": formatDataSource}
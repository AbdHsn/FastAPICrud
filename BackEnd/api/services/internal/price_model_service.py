from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.price_model_model import PriceModel
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.price_model_schema import PriceModelCreate, PriceModelUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_price_model_view_model import GetPriceModelsView
import json

router = APIRouter()

@router.get("/get-price-models")
async def get_price_models_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PriceModel)
    price_models = await repo.get_all()
    if not price_models:
        raise HTTPException(status_code=404, detail="Price models not found")
    return price_models

@router.get("/get-price-model-by-id")
async def get_price_model_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PriceModel)
    price_model = await repo.get_by_field(price_model_id=id)
    if not price_model:
        raise HTTPException(status_code=404, detail="Price model not found")
    return price_model

@router.post("/create-price-model", status_code=201)
async def create_price_model_endpoint(price_model_data: PriceModelCreate, db: AsyncSession = Depends(get_session)):
    new_price_model = PriceModel(**price_model_data.dict())
    repo = GenericRepository(db, PriceModel)
    new_price_model = await repo.insert(new_price_model)
    return new_price_model

@router.put("/update-price-model")
async def update_price_model_endpoint(id: int, price_model_data: PriceModelUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PriceModel)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = price_model_data.dict(exclude_unset=True)

    updated_price_model = await repo.update('price_model_id', id, **update_data)
    if not updated_price_model:
        raise HTTPException(status_code=404, detail="Price model not found")
    return updated_price_model

@router.delete("/delete-price-model")
async def delete_price_model_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, PriceModel)
    success = await repo.delete('price_model_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="Price model not found")
    return {"message": "Price model deleted successfully"}

@router.get("/get-price-models-view")
async def get_price_models_view_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetPriceModelsView)
    price_models_view = await repo.get_all()
    if not price_models_view:
        raise HTTPException(status_code=404, detail="Price models view not found")
    return price_models_view

@router.get("/get-price-model-grid-by-id")
async def get_price_model_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetPriceModelsView)
    price_model = await repo.get_by_field(price_model_id=id)
    if not price_model:
        raise HTTPException(status_code=404, detail="Price model not found")
    return price_model

@router.post("/get-price-model-grid")
async def get_price_model_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "price_model_id DESC"  # Default sort
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
    dataGrid.table_or_view_name = "GetPriceModelsView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetPriceModelsView)
    data = await repo.get_all_by_where(dataGrid)

    formatDataSource = []
    for price_model in data:
        price_model_dict = dict(price_model)
        formatDataSource.append(price_model_dict)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetPriceModelsView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "price_model_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": formatDataSource}
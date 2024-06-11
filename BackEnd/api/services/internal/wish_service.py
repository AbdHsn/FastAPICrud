from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.wish_model import Wish
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.wish_schema import WishCreate, WishUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_wish_view_model import GetWishesView
import json

router = APIRouter()

@router.get("/get-wishes")
async def get_wishes_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Wish)
    wishes = await repo.get_all()
    if not wishes:
        raise HTTPException(status_code=404, detail="Wishes not found")
    return wishes

@router.get("/get-wish-by-id")
async def get_wish_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Wish)
    wish = await repo.get_by_field(wish_id=id)
    if not wish:
        raise HTTPException(status_code=404, detail="Wish not found")
    return wish

@router.post("/create-wish", status_code=201)
async def create_wish_endpoint(wish_data: WishCreate, db: AsyncSession = Depends(get_session)):
    new_wish = Wish(**wish_data.dict())
    repo = GenericRepository(db, Wish)
    new_wish = await repo.insert(new_wish)
    return new_wish

@router.put("/update-wish")
async def update_wish_endpoint(id: int, wish_data: WishUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Wish)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = wish_data.dict(exclude_unset=True)

    updated_wish = await repo.update('wish_id', id, **update_data)
    if not updated_wish:
        raise HTTPException(status_code=404, detail="Wish not found")
    return updated_wish

@router.delete("/delete-wish")
async def delete_wish_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Wish)
    success = await repo.delete('wish_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="Wish not found")
    return {"message": "Wish deleted successfully"}

@router.get("/get-wishes-view")
async def get_wishes_view_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetWishesView)
    wishes_view = await repo.get_all()
    if not wishes_view:
        raise HTTPException(status_code=404, detail="Wishes view not found")
    return wishes_view

@router.get("/get-wish-grid-by-id")
async def get_wish_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetWishesView)
    wish = await repo.get_by_field(wish_id=id)
    if not wish:
        raise HTTPException(status_code=404, detail="Wish not found")
    return wish

@router.post("/get-wish-grid")
async def get_wish_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "wish_id DESC"  # Default sort
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
    dataGrid.table_or_view_name = "GetWishesView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetWishesView)
    data = await repo.get_all_by_where(dataGrid)

    formatDataSource = []
    for wish in data:
        wish_dict = dict(wish)
        formatDataSource.append(wish_dict)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetWishesView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "wish_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": formatDataSource}
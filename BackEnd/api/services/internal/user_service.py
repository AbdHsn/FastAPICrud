from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user_model import User
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.user_schema import UserCreate, UserUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_user_view_model import GetUsersView

router = APIRouter()

@router.get("/get-users")
async def get_users_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, User)
    users = await repo.get_all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@router.get("/get-user-by-id")
async def get_user_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, User)
    user = await repo.get_by_field(user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create-user", status_code=201)
async def create_user_endpoint(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    new_user = User(**user_data.dict())
    repo = GenericRepository(db, User)
    new_user = await repo.insert(new_user)
    return new_user

@router.put("/update-user")
async def update_user_endpoint(id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, User)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = user_data.dict(exclude_unset=True)

    updated_user = await repo.update('user_id', id, **update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/delete-user")
async def delete_user_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, User)
    success = await repo.delete('user_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/get-user-grid-by-id")
async def get_user_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetUsersView)
    user = await repo.get_by_field(user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/get-user-grid")
async def get_user_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "user_id DESC"  # Default sort
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
    dataGrid.table_or_view_name = "GetUsersView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetUsersView)
    data = await repo.get_all_by_where(dataGrid)

    formatDataSource = []
    for user in data:
        user_dict = dict(user)
        formatDataSource.append(user_dict)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetUsersView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "user_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": formatDataSource}
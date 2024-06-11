from fastapi import APIRouter, Depends, HTTPException
from db.db_config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.vehicle_type_model import VehicleType
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.vehicle_type_schema import VehicleTypeCreate, VehicleTypeUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_vehicle_type_view_model import GetVehicleTypesView

router = APIRouter()

@router.get("/get-vehicle-types")
async def get_vehicle_types_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, VehicleType)
    vehicle_types = await repo.get_all()
    if not vehicle_types:
        raise HTTPException(status_code=404, detail="Vehicle types not found")
    return vehicle_types

@router.get("/get-vehicle-type-by-id")
async def get_vehicle_type_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, VehicleType)
    vehicle_type = await repo.get_by_field(vehicle_type_id=id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return vehicle_type

@router.post("/create-vehicle-type", status_code=201)
async def create_vehicle_type_endpoint(vehicle_type: VehicleTypeCreate, db: AsyncSession = Depends(get_session)):
    new_vehicle_type = VehicleType()
    new_vehicle_type.name = vehicle_type.name
    repo = GenericRepository(db, VehicleType)
    new_vehicle_type = await repo.insert(new_vehicle_type)
    return new_vehicle_type

@router.put("/update-vehicle-type")
async def update_vehicle_type_endpoint(id: int, vehicle_type_data: VehicleTypeUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, VehicleType)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = vehicle_type_data.dict(exclude_unset=True)

    updated_vehicle_type = await repo.update('vehicle_type_id', id, **update_data)
    if not updated_vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return updated_vehicle_type

@router.delete("/delete-vehicle-type")
async def delete_vehicle_type_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, VehicleType)
    success = await repo.delete('vehicle_type_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return {"message": "Vehicle type deleted successfully"}

@router.post("/get-vehicle-types-grid")
async def get_vehicle_type_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "vehicle_type_id DESC"  # Default sort
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
    dataGrid.table_or_view_name = "GetVehicleTypesView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetVehicleTypesView)
    data = await repo.get_all_by_where(dataGrid)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetVehicleTypesView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "vehicle_type_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": data}

    
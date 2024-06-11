from fastapi import APIRouter, Depends, HTTPException
from db.db_config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.vehicle_model import Vehicle
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.vehicle_schema import VehicleCreate, VehicleUpdate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_vehicle_view_model import GetVehiclesView
import json
import os
import shutil  # Add this line to import shutil module
from fastapi import UploadFile, File
from typing import List
import json


UPLOAD_DIRECTORY = "static/images/"
router = APIRouter()

@router.get("/get-vehicles")
async def get_vehicles_endpoint(db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Vehicle)
    lst = await repo.get_all()
    if not lst:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return lst

@router.get("/get-vehicle-by-id")
async def get_vehicle_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Vehicle)
    obj = await repo.get_by_field(vehicle_id=id)
    if not obj:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return obj

def save_image(file: UploadFile) -> str:
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

@router.post("/create-vehicle", status_code=201)
async def create_vehicle_endpoint(vehicle: VehicleCreate, db: AsyncSession = Depends(get_session)):
    # Create instance of Vehicle model
    new_obj = Vehicle()
    new_obj.name = vehicle.title

    # Save image files and generate JSON string
    # images_data = {}
    # for image_file in image_files:
    #     image_path = save_image(image_file)
    #     image_name = image_file.filename.split(".")[0]
    #     images_data[image_name] = image_path

    #print(images_data)

    # Convert images data to JSON string
    #images_json = ""#json.dumps(images_data)

    # Update vehicle object with images JSON string
    #new_obj.images = images_json

    # Insert vehicle
    repo = GenericRepository(db, Vehicle)
    new_obj = await repo.insert(new_obj)
    
    return new_obj

# @router.post("/create-vehicle", status_code=201)
# async def create_vehicle_endpoint(vehicle_type: VehicleCreate, db: AsyncSession = Depends(get_session)):
#     new_obj = Vehicle()
#     new_obj.name = vehicle_type.name
#     new_obj.images = ""
#     repo = GenericRepository(db, Vehicle)
#     new_obj = await repo.insert(new_obj)
#     return new_obj

@router.put("/update-vehicle")
async def update_vehicle_endpoint(id: int, vehicle_data: VehicleUpdate, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Vehicle)

    # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
    update_data = vehicle_data.dict(exclude_unset=True)

    updated_vehicle = await repo.update('vehicle_id', id, **update_data)
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle

@router.delete("/delete-vehicle")
async def delete_vehicle_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, Vehicle)
    success = await repo.delete('vehicle_id', id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": "Vehicle deleted successfully"}


# @router.get("/get-vehicle-grid-by-id")
# async def get_vehicle_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
#     repo = GenericRepository(db, GetVehiclesView)
#     obj = await repo.get_by_field(vehicle_id=id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
#     return obj

@router.get("/get-vehicle-grid-by-id")
async def get_vehicle_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, GetVehiclesView)
    obj = await repo.get_by_field(vehicle_id=id)

    if not obj:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Create dictionary manually
    vehicle_dict = {
        "vehicle_id": obj.vehicle_id,
        "title": obj.title,
        "description": obj.description,
        "vehicle_model_id": obj.vehicle_model_id,
        "vehicle_model": obj.vehicle_model,
        "vehicle_type_id": obj.vehicle_type_id,
        "vehicle_type": obj.vehicle_type,
        "vehicle_color_id": obj.vehicle_color_id,
        "vehicle_color": obj.vehicle_color,
        "price_model_id": obj.price_model_id,
        "price_model": obj.price_model,
        "price": obj.price,
        "vin": obj.vin,
        "year": obj.year,
        "images": json.loads(obj.images) if obj.images else [],
        "status": obj.status,
        "created_at": obj.created_at
    }

    return vehicle_dict

@router.post("/get-vehicle-grid")
async def get_vehicle_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "vehicle_id DESC"  # Default sort
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
    dataGrid.table_or_view_name = "GetVehiclesView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetVehiclesView)
    data = await repo.get_all_by_where(dataGrid)

    formatDataSource = []
    for vehicle in data:
        vehicle_dict = dict(vehicle)
        vehicle_dict['images'] = json.loads(vehicle.images) if vehicle.images else []
        formatDataSource.append(vehicle_dict)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetVehiclesView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "vehicle_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": formatDataSource}

    
from fastapi import APIRouter, Depends, HTTPException
from db.db_config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
# from db.models.view_models import get_order_view_model
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.order_schema import OrderCreate
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB
from schemas.datatable_schema import DatatableGLB
from db.models.view_models.get_order_view_model import GetOrdersView
from db.models.order_model import Orders
from db.models.user_model import User
from db.models.contract_model import Contract
from db.models.address_model import Address
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from db.models.credit_application_model import CreditApplication
from db.models.contract_model import Contract
# from schemas.credit_application_schema import CreditApplicationCreate
# from schemas.contract_schema import ContractCreate

router = APIRouter()

@router.post("/create-order", status_code=201)
async def create_order_endpoint(order: OrderCreate, db: AsyncSession = Depends(get_session)):
    
    # repo_user = GenericRepository(db, User)
    # userExistByEmail = await repo_user.get_by_field(email=order.email)
    # userExistByPhone = await repo_user.get_by_field(phone=order.phone)

    # if userExistByPhone or userExistByEmail:
    #     raise HTTPException(status_code=404, detail="Users not found")
   
    # Create instance of Orders model
    new_order = Orders()
    new_order.user_id = order.user_id
    new_order.vehicle_id = order.vehicle_id
    new_order.price = order.price
    new_order.status = "pending"
    new_order.gateway_id = order.gateway_id
    new_order.payment_status = order.payment_status
    new_order.start_date = order.start_date.strftime('%Y-%m-%d %H:%M:%S')
    new_order.end_date = order.end_date.strftime('%Y-%m-%d %H:%M:%S')
    new_order.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Insert order
    repo_order = GenericRepository(db, Orders)
    await repo_order.insert(new_order)

    new_credit_application = CreditApplication()
    new_credit_application.order_id = new_order.order_id
    new_credit_application.address_id = 1
    new_credit_application.first_name = order.credit_name
    new_credit_application.last_name = order.credit_last_name
    new_credit_application.birth_date = order.credit_birth_date.strftime('%Y-%m-%d %H:%M:%S')
    new_credit_application.marital_status = order.credit_marital_status
    new_credit_application.email = order.credit_email
    new_credit_application.phone = order.credit_phone
    new_credit_application.TIN = order.credit_tin
    # Insert credit application
    repo_credit_application = GenericRepository(db, CreditApplication)
    await repo_credit_application.insert(new_credit_application)

    new_contract = Contract()
    new_contract.order_id = new_order.order_id
    new_contract.user_id = new_order.user_id
    new_contract.e_sign = order.contract_sign
    new_contract.sign_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_contract.policy_id = 1
    new_contract.policy = order.contract_policy
    new_contract.status = "signed"
    # Insert contract application
    repo_contract = GenericRepository(db, Contract)
    await repo_contract.insert(new_contract)

    new_address = Address()
    new_address.user_id = new_order.user_id
    new_address.address_type = "default"
    new_address.street = order.street
    new_address.city = order.city
    new_address.state = order.state
    new_address.postal_code = order.postal_code
    # Insert address 
    repo_address = GenericRepository(db, Address)
    await repo_address.insert(new_address)

    # Convert the Pydantic model to a dictionary
    order_dict = order.dict()
    # Add the additional property to the dictionary
    order_dict['order_id'] = new_order.order_id
    # Create a new instance of OrderCreate with the updated dictionary
    order_created = OrderCreate(**order_dict)
        
    return order_created

# @router.post("/create-order", status_code=201)
# async def create_order_endpoint(order: OrderCreate, db: AsyncSession = Depends(get_session)):
    
    # repo_user = GenericRepository(db, User)
    # userExistByEmail = await repo_user.get_by_field(email=order.email)
    # userExistByPhone = await repo_user.get_by_field(phone=order.phone)

    # if userExistByPhone or userExistByEmail:
    #     raise HTTPException(status_code=404, detail="Users not found")

    # try:
    #     async with db.begin():
    
    #         # Create instance of Orders model
    #         new_order = Orders()
    #         new_order.user_id = order.user_id
    #         new_order.vehicle_id = order.vehicle_id
    #         new_order.price = order.price
    #         new_order.status = "pending"
    #         new_order.gateway_id = order.gateway_id
    #         new_order.payment_status = order.payment_status
    #         new_order.start_date = order.start_date.strftime('%Y-%m-%d %H:%M:%S')
    #         new_order.end_date = order.end_date.strftime('%Y-%m-%d %H:%M:%S')
    #         new_order.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         # Insert order
    #         repo_order = GenericRepository(db, Orders)
    #         await repo_order.insert(new_order)

    #         new_credit_application = CreditApplication()
    #         new_credit_application.order_id = new_order.order_id
    #         new_credit_application.address_id = 1
    #         new_credit_application.first_name = order.credit_name
    #         new_credit_application.last_name = order.credit_last_name
    #         new_credit_application.birth_date = order.credit_birth_date.strftime('%Y-%m-%d %H:%M:%S')
    #         new_credit_application.marital_status = order.credit_marital_status
    #         new_credit_application.email = order.credit_email
    #         new_credit_application.phone = order.credit_phone
    #         new_credit_application.TIN = order.credit_tin
    #         # Insert credit application
    #         repo_credit_application = GenericRepository(db, CreditApplication)
    #         await repo_credit_application.insert(new_credit_application)

    #         new_contract = Contract()
    #         new_contract.order_id = new_order.order_id
    #         new_contract.user_id = new_order.user_id
    #         new_contract.e_sign = order.contract_sign
    #         new_contract.sign_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         new_contract.policy_id = 1
    #         new_contract.policy = order.contract_policy
    #         new_contract.status = "signed"
    #         # Insert contract application
    #         repo_contract = GenericRepository(db, Contract)
    #         await repo_contract.insert(new_contract)

    #         new_address = Address()
    #         new_address.user_id = new_order.user_id
    #         new_address.address_type = "default"
    #         new_address.street = order.street
    #         new_address.city = order.city
    #         new_address.state = order.state
    #         new_address.postal_code = order.postal_code
    #         # Insert address 
    #         repo_address = GenericRepository(db, Address)
    #         await repo_address.insert(new_address)
                
    #         return new_order
    # except SQLAlchemyError as e:
    #     # Roll back the transaction in case of error
    #     await db.rollback()
    #     print(e)
    #     raise HTTPException(status_code=500, detail="Order creation failed.")


# @router.post("/create-order", status_code=201)
# async def create_order_endpoint(order: OrderCreate, db: AsyncSession = Depends(get_session)):
#     # new_order = Orders()
#     # repo = GenericRepository(db, Orders)
#     # new_obj = await repo.insert(new_obj)
#     # return new_obj

#     try:
#         async with db.begin():
#             # Create instance of Orders model
#             new_order = Orders()
#             new_order.user_id = order.user_id
#             new_order.vehicle_id = order.vehicle_id
#             new_order.price = order.price
#             new_order.status = order.status
#             new_order.gateway_id = order.gateway_id
#             new_order.payment_status = order.payment_status
#             new_order.start_date = order.start_date.strftime('%Y-%m-%d %H:%M:%S')
#             new_order.end_date = order.end_date.strftime('%Y-%m-%d %H:%M:%S')
#             new_order.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#             new_credit_application = CreditApplication()
#             new_credit_application.order_id = new_order.order_id
#             new_credit_application.address_id = 1
#             new_credit_application.first_name = order.credit_name
#             new_credit_application.last_name = order.credit_last_name
#             new_credit_application.birth_date = order.credit_birth_date.strftime('%Y-%m-%d %H:%M:%S')
#             new_credit_application.marital_status = order.credit_marital_status
#             new_credit_application.email = order.credit_email
#             new_credit_application.phone = order.credit_phone
#             new_credit_application.TIN = order.credit_tin

#             # Insert order
#             repo_order = GenericRepository(db, Orders)
#             await repo_order.insert(new_order)
            
#             # Insert credit application
#             repo_credit_application = GenericRepository(db, CreditApplication)
#             await repo_credit_application.insert(new_credit_application)
            
#             # # Create instance of CreditApplication model
#             # new_credit_application = CreditApplication(**credit_application.dict(), order_id=new_order.order_id)
            
#             # # Create instance of Contract model
#             # new_contract = Contract(**contract.dict(), order_id=new_order.order_id)
            
#             # # Insert order
#             # repo_order = GenericRepository(db, Orders)
#             # await repo_order.insert(new_order)
            
#             # # Insert credit application
#             # repo_credit_application = GenericRepository(db, CreditApplication)
#             # await repo_credit_application.insert(new_credit_application)
            
#             # # Insert contract
#             # repo_contract = GenericRepository(db, Contract)
#             # await repo_contract.insert(new_contract)
            
#             return new_order
#     except SQLAlchemyError as e:
#         # Roll back the transaction in case of error
#         await db.rollback()
#         print(e)
#         raise HTTPException(status_code=500, detail="Order creation failed.")


# @router.get("/get-vehicles")
# async def get_vehicles_endpoint(db: AsyncSession = Depends(get_session)):
#     repo = GenericRepository(db, Vehicle)
#     lst = await repo.get_all()
#     if not lst:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
#     return lst

# @router.get("/get-vehicle-by-id")
# async def get_vehicle_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
#     repo = GenericRepository(db, Vehicle)
#     obj = await repo.get_by_field(vehicle_id=id)
#     if not obj:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
#     return obj



# @router.put("/update-vehicle")
# async def update_vehicle_endpoint(id: int, vehicle_data: VehicleUpdate, db: AsyncSession = Depends(get_session)):
#     repo = GenericRepository(db, Vehicle)

#     # Convert Pydantic model to dictionary, excluding unset values and SQLAlchemy models
#     update_data = vehicle_data.dict(exclude_unset=True)

#     updated_vehicle = await repo.update('vehicle_id', id, **update_data)
#     if not updated_vehicle:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
#     return updated_vehicle

# @router.delete("/delete-vehicle")
# async def delete_vehicle_endpoint(id: int, db: AsyncSession = Depends(get_session)):
#     repo = GenericRepository(db, Vehicle)
#     success = await repo.delete('vehicle_id', id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
#     return {"message": "Vehicle deleted successfully"}


# @router.get("/get-vehicle-grid-by-id")
# async def get_vehicle_grid_by_id_endpoint(id: int, db: AsyncSession = Depends(get_session)):
#     repo = GenericRepository(db, GetVehiclesView)
#     obj = await repo.get_by_field(vehicle_id=id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Vehicle not found")

#     # Create dictionary manually
#     vehicle_dict = {
#         "vehicle_id": obj.vehicle_id,
#         "title": obj.title,
#         "description": obj.description,
#         "vehicle_model_id": obj.vehicle_model_id,
#         "vehicle_model": obj.vehicle_model,
#         "vehicle_type_id": obj.vehicle_type_id,
#         "vehicle_type": obj.vehicle_type,
#         "vehicle_color_id": obj.vehicle_color_id,
#         "vehicle_color": obj.vehicle_color,
#         "price_model_id": obj.price_model_id,
#         "price_model": obj.price_model,
#         "price": obj.price,
#         "vin": obj.vin,
#         "year": obj.year,
#         "images": json.loads(obj.images) if obj.images else [],
#         "status": obj.status,
#         "created_at": obj.created_at
#     }

#     return vehicle_dict

@router.post("/get-order-grid")
async def get_order_grid_endpoint(table_obj: DatatableGLB, db: AsyncSession = Depends(get_session)):
    # Parse row size
    row_size = 0 if table_obj.length == "All" else int(table_obj.length)

    # Determine sort information
    sort_information = "order_id DESC"  # Default sort
    if table_obj.orders and len(table_obj.orders) > 0:
        sort_information = f"{table_obj.orders[0].column} {table_obj.orders[0].order_by}"

    # Build where condition
    where_conditions = []
    for search in table_obj.searches or []:
        if search.search_by == "created_at" and search.fromdate and search.todate:
            where_conditions.append(f"(created_at BETWEEN '{search.fromdate}' AND '{search.todate}')")
        elif search.value:
            where_conditions.append(f"{search.search_by} LIKE '%{search.value}%'")

    where_clause = " AND ".join(where_conditions)
    where_clause = f" {where_clause}" if where_conditions else ""

    print("where condition: ", where_clause, where_conditions)

    dataGrid = GetAllByWhereGLB()
    dataGrid.table_or_view_name = "GetOrdersView"
    dataGrid.sort_column = sort_information
    dataGrid.where_conditions = where_clause
    dataGrid.limit_index = table_obj.start
    dataGrid.limit_range = row_size

    repo = GenericRepository(db, GetOrdersView)
    data = await repo.get_all_by_where(dataGrid)

    gridCount = CountByWhereGLB()
    gridCount.table_or_view_name = "GetOrdersView"
    gridCount.where_conditions = where_clause
    gridCount.column_name = "order_id"
    total_record = await repo.count_all_by_where(gridCount)

    if not data:
        {"total_record": total_record, "data": []}
    return {"total_record": total_record, "data": data}

    
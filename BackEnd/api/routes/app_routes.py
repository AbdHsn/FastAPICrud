from fastapi import APIRouter, Depends, Request, HTTPException, status
from db.models.user_model import User
from services.v1 import user_type_service
from services.internal import user_type_service as user_type_service
from services.internal import vehicle_type_service
from services.internal import vehicle_service
from services.internal import user_service
from services.internal import payment_gateway_service
from services.internal import policy_service
from services.internal import price_model_service
from services.internal import wish_service
from services.internal import order_service
from services.public import account_service

async def get_current_user(request: Request):
    if request.state.user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return request.state.user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.user_type_id != 1:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

def customer_required(current_user: User = Depends(get_current_user)):
    if current_user.user_type_id != 3:
        raise HTTPException(status_code=403, detail="Customer privileges required")
    return current_user


app_router = APIRouter()

@app_router.get("/")
def app_working():
    return {"message" : "Backend API working."}

#app_router.include_router(user_type_service.router, prefix="/user-type", tags=["User Type"], dependencies=[Depends(get_current_user)])
app_router.include_router(account_service.router, prefix="/account", tags=["Account"])

app_router.include_router(vehicle_type_service.router, prefix="/vehicle-type", tags=["Vehicle Type"])
app_router.include_router(vehicle_service.router, prefix="/vehicle", tags=["Vehicle"])

app_router.include_router(user_type_service.router, prefix="/user-type", tags=["User Type"])
app_router.include_router(user_service.router, prefix="/user", tags=["User"])
app_router.include_router(payment_gateway_service.router, prefix="/payment-gateway", tags=["Payment Gateway"])
app_router.include_router(policy_service.router, prefix="/policy", tags=["Policy"])
app_router.include_router(price_model_service.router, prefix="/price-model", tags=["Price Model"])
app_router.include_router(wish_service.router, prefix="/wish", tags=["Wish"])
app_router.include_router(order_service.router, prefix="/order", tags=["Order"])



# # Admin Routes - Require admin privileges
# @app_router.get("/route", dependencies=[Depends(admin_required)])
# async def admin_route():
#     return {"message": "Admin access granted"}

# # Customer Routes - Require customer privileges
# @app_router.get("/customer/route", dependencies=[Depends(customer_required)])
# async def customer_route():
#     return {"message": "Customer access granted"}
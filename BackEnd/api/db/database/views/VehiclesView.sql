-- GetVehiclesView source

CREATE VIEW GetVehiclesView
AS
SELECT 
v.vehicle_id, 
v.title,
v.description,
v.vehicle_model_id, 
vm.name vehicle_model, 
v.vehicle_type_id, 
vt.name vehicle_type,
v.vehicle_color_id, 
vc.name vehicle_color,
v.price_model_id, 
pm.name price_model,
pm.price, 
v.vin, 
v."year", 
v.images,
v.status, 
v.created_at  
FROM Vehicle v 
LEFT JOIN VehicleModel vm ON v.vehicle_model_id = vm.vehicle_model_id
LEFT JOIN VehicleType vt ON v.vehicle_type_id = vt.vehicle_type_id
LEFT JOIN VehicleColor vc ON v.vehicle_color_id = vc.vehicle_color_id
LEFT JOIN PriceModel pm ON v.price_model_id = pm.price_model_id;
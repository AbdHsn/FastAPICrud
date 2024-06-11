create view GetUsersView
AS
select 
u.user_id, 
u.user_type_id, 
ut.name user_type,
u.email, 
u.phone, 
u.first_name, 
u.last_name, 
u.birth_date 
from "User" u
left join UserType ut on u.user_type_id = ut.user_type_id 
from app import api
from app.resources.users import UserResource, UserListResource


route = api.add_resource

route(UserListResource, '/users')
route(UserResource, '/users/<int:user_id>')
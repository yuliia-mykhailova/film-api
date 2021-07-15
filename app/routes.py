from app import api
from app.resources.users import UserResource, UserListResource
from app.resources.directors import DirectorResource, DirectorListResource


route = api.add_resource

route(UserListResource, '/users')
route(UserResource, '/users/<int:user_id>')

# route(DirectorListResource, '/directors')
# route(DirectorResource, '/director/<int:director_id>')

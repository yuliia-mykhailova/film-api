from app import api
from app.resources.users import UserResource, UserListResource
from app.resources.directors import DirectorResource, DirectorListResource
from app.resources.genres import GenreResource, GenreListResource


route = api.add_resource

route(UserListResource, '/users')
route(UserResource, '/users/<int:user_id>')

route(DirectorListResource, '/directors')
route(DirectorResource, '/directors/<int:director_id>')

route(GenreListResource, '/genres')
route(GenreResource, '/genres/<int:genre_id>')

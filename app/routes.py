"""Module for project routes"""

from app import api

from app.resources.login_logout import LoginResource, LogoutResource
from app.resources.users import UserResource, UserListResource
from app.resources.directors import DirectorResource, DirectorListResource
from app.resources.genres import GenreResource, GenreListResource
from app.resources.films import FilmResource, FilmListResource


route = api.add_resource


route(LoginResource, '/login')
route(LogoutResource, '/logout')

route(UserListResource, '/users')
route(UserResource, '/users/<int:user_id>')

route(DirectorListResource, '/directors')
route(DirectorResource, '/directors/<int:director_id>')

route(GenreListResource, '/genres')
route(GenreResource, '/genres/<int:genre_id>')

route(FilmListResource, '/films')
route(FilmResource, '/films/<int:film_id>')

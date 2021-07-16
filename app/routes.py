from app import api
from app.resources.login_logout import LoginResource, LogoutResource


route = api.add_resource

route(LoginResource, '/login')
route(LogoutResource, '/logout')

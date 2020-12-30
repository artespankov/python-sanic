from typing import Dict
from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound, InvalidUsage
from schematics.exceptions import BaseError
from sanic_transmute import describe, add_swagger, add_route

from models import User

web_app = Sanic()


def sanic_error_handler(status):
    async def custom_error_handler(request, exception):
        return response.json({'success': False, 'error': str(exception)}, status=status)
    return custom_error_handler


web_app.error_handler.add(BaseError, sanic_error_handler(400))
web_app.error_handler.add(NotFound, sanic_error_handler(404))
web_app.error_handler.add(InvalidUsage, sanic_error_handler(400))
web_app.error_handler.add(Exception, sanic_error_handler(500))


@web_app.route(methods=['GET'], uri='/users/<user_id>')
async def get_user_by_id(request, user_id: int):
    # user = await db.get_user_by_id(user_id)
    return response.json({'user_id': user_id})


@web_app.route(methods=['POST'], uri='/users')
async def add_user(request):
    user = User(request.json, strict=True)
    user.validate()
    # user = await db.add_user(user.to_native())
    return response.json({'user_id': user.user_id}, status=200)


@web_app.route(methods=['PUT'], uri='/users/<user_id>')
async def update_user_by_id(request, user_id: int, user: User) -> Dict:
    # user = await db.update_user_by_id(user_id, request.json)
    return {'user_id': user_id}


# Redirect
@web_app.route('/follow')
def handle_request(request):
    return response.redirect('/redirect')

@web_app.route('/redirect')
async def test(request):
    return response.json({"Redirected": True})


# named url
@web_app.route('/named-redirect')
async def index(request):
    # generate a URL for the endpoint `update_user_by_id` handler
    url = web_app.url_for('update_user_by_id', user_id=5)
    return response.redirect(url)


if __name__ == "__main__":
    # add swagger
    # add_route(web_app, get_user_by_id)
    # add_swagger(web_app, "/swagger.json", "/api")
    web_app.run(host="0.0.0.0", port=8080, auto_reload=True)


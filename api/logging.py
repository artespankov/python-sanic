from sanic import Sanic
from sanic import response
import logging

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)
log = logging.getLogger()

# Set logger to override default basicConfig
sanic = Sanic()


@sanic.route("/")
def test(request):
    log.info("received request; responding with 'hey'")
    return response.text("hey")

sanic.run(host="0.0.0.0", port=8000)
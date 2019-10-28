from aiohttp import web
import aiohttp_cors
import asyncio
import signal
import logging

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

from . import config, exceptions, signal_handler, __version__
from .server_commands import connect_to_gateway

from .routes import routes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def start(hostConfig):
    global APP_FACTORY
    loop = asyncio.get_event_loop()

    app = web.Application()
    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    try:
        app["api"], app["gateway"], APP_FACTORY = await connect_to_gateway(hostConfig)

        app.add_routes(routes)
        for route in list(app.router.routes()):
            cors.add(route)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, hostConfig["Server_ip"], hostConfig["Http_port"])

        logger.info(
            "Starting IKEA-Tradfri HTTP server {2} on {0}:{1}".format(
                hostConfig["Server_ip"], hostConfig["Http_port"], __version__
            )
        )
        await site.start()

    except exceptions.ConfigNotFound:
        await signal_handler.shutdown("ERROR")

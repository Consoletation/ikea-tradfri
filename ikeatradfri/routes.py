from aiohttp import web

from aiohttp_cors import CorsConfig, APP_CONFIG_KEY
from aiohttp_cors import ResourceOptions, CorsViewMixin, custom_cors

try:
    from . import devices as Devices
    from . import server_commands as Server_Commands
except ImportError:
    import devices as Devices
    import server_commands as Server_Commands

import json

routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return web.Response(text="Hello, world")


@routes.get("/devices")
async def listdevices(request):
    devices = []
    lights, outlets, groups, others = await Devices.get_devices(
        request.app["api"], request.app["gateway"]
    )

    for aDevice in lights:
        devices.append(aDevice.description)

    for aDevice in outlets:
        devices.append(aDevice.description)

    for aGroup in groups:
        devices.append(aGroup.description)

    for aDevice in others:
        devices.append(aDevice.description)

    return web.Response(text=json.dumps(devices))


@routes.view("/devices/{id}")
class DeviceView(web.View, CorsViewMixin):
    cors_config = {
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    }

    async def get(self):
        device = await Devices.get_device(
            self.request.app["api"],
            self.request.app["gateway"],
            self.request.match_info["id"],
        )
        # print(json.dumps(device))
        # return web.json_response(device)
        return web.json_response(device.description)

    async def put(self):
        if self.request.body_exists:
            try:
                return web.json_response(await Server_Commands.serverCommand(self.request))
            except TypeError:  # Can't serialize, bypass for now
                return web.json_response(None)
        else:
            return web.json_response(
                Server_Commands.return_object(
                    status="Error", result="No PUT-data given"
                )
            )

        return web.json_response(Server_Commands.returnObject)


@routes.get("/lights")
async def listlights(request):
    devices = []
    lights, outlets, groups, others = await Devices.getDevices(
        request.app["api"], request.app["gateway"]
    )

    for aDevice in lights:
        devices.append(
            {
                "DeviceID": aDevice.id,
                "Name": aDevice.name,
                "Type": "Light",
                "Dimmable": aDevice.light_control.can_set_dimmer,
                "HasWB": aDevice.light_control.can_set_temp,
                "HasRGB": aDevice.light_control.can_set_xy,
            }
        )

    return web.Response(text=json.dumps(devices))


@routes.get("/outlets")
async def listOutlets(request):
    devices = []
    lights, outlets, groups, others = await Devices.getDevices(
        request.app["api"], request.app["gateway"]
    )

    for aDevice in outlets:
        devices.append(
            {
                "DeviceID": aDevice.id,
                "Name": aDevice.name,
                "Type": "Outlet",
                "Dimmable": False,
                "HasWB": False,
                "HasRGB": False,
            }
        )

    return web.Response(text=json.dumps(devices))


@routes.get("/groups")
async def listGroups(request):
    devices = []
    lights, outlets, groups, others = await Devices.getDevices(
        request.app["api"], request.app["gateway"]
    )

    for aGroup in groups:
        devices.append({"DeviceID": aGroup.id, "Name": aGroup.name, "Type": "Group"})

    return web.Response(text=json.dumps(devices))

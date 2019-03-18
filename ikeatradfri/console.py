from .devices import getDevices


async def listDevices(api, gateway):
    lights, outlets, groups, others = await getDevices(api, gateway)
    print("Lights:")
    for aDevice in lights:
        print("{0}: {1} ({2}) - {3}".
              format(aDevice.id, aDevice.name,
                     aDevice.device_info.model_number,
                     aDevice.light_control.lights[0].state))

    print("\nSockets:")
    for aDevice in outlets:
        print("{0}: {1} ({2}) - {3}".
              format(aDevice.id, aDevice.name,
                     aDevice.device_info.model_number,
                     aDevice.socket_control.sockets[0].state))

    print("\nDevices:")
    for aDevice in others:
        print("{0}: {1} ({2}) - {3}".
              format(aDevice.id, aDevice.name,
                     aDevice.device_info.model_number,
                     aDevice.device_info.battery_level))

    print("\nGroups:")
    for aGroup in groups:
        print("{0}: {1}".format(aGroup.id, aGroup.name))
    return

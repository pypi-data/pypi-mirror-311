import asyncio

from bleak import BleakScanner


async def discover_devices():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)


asyncio.run(discover_devices())

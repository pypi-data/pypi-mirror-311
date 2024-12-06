import asyncio
import time

from bleak import BleakClient, BleakScanner


class DeviceNotFoundError(Exception):
    pass


class WT9011:
    # GATT characteristics:
    # Notify characteristic UUID
    CHAR_NOTIFY = "0000ffe4-0000-1000-8000-00805f9a34fb"
    # Write characteristic UUID
    CHAR_WRITE = "0000ffe9-0000-1000-8000-00805f9a34fb"

    DESCRIPTOR = "00002902-0000-1000-8000-00805f9b34fb"

    # Request battery info
    REQ_BAT_INFO = bytearray([0xFF, 0xAA, 0x27, 0x64, 0x00])

    # Header and flags:
    PACKET_HEADER = 0x55
    # Flag in a frame containing inertial data
    FLAG_INERTIAL = 0x61
    # Flag in a frame containing battery data
    FLAG_BATTERY = 0x71

    def __init__(self, address, name):
        if address is None and name is None:
            raise Exception("Either address or name must be specified to create a sensor")
        self.address = address
        self.name = name

    async def _find_device(self):
        print("Starting the scan...")
        if self.address:
            device = await BleakScanner.find_device_by_address(self.address)
            if device is None:
                print(f"Could not find the device with address '{self.address}'")
                raise DeviceNotFoundError
        else:
            device = await BleakScanner.find_device_by_name(self.name)
            if device is None:
                print(f"Could not find the device with name '{self.name}")
                raise DeviceNotFoundError
        return device

    async def _listen_for_notifies(self, queue: asyncio.Queue, client: BleakClient):

        # TODO: make callback_handler a class method?
        # TODO: make queue a class field?
        async def callback_handler(_, data):
            await queue.put((time.time(), data))

        # TODO: run until stopped with ctrl-c instead of running 10 seconds
        print("Listening for notifies for 10 seconds")
        await client.start_notify(WT9011.CHAR_NOTIFY, callback_handler)
        await asyncio.sleep(10.0)
        await client.stop_notify(WT9011.CHAR_NOTIFY)

    async def _get_battery_level(self, queue: asyncio.Queue, client: BleakClient):

        async def callback_handler(_, data):
            await queue.put((time.time(), data))

        print("Getting battery level")
        # Using this notify hack instead of getting a proper response from write (response = await client.write_gatt_char())
        # because of this issue https://github.com/hbldh/bleak/issues/59
        await client.start_notify(WT9011.CHAR_NOTIFY, callback_handler)
        await client.write_gatt_char(WT9011.CHAR_WRITE, self.REQ_BAT_INFO, response=True)
        await asyncio.sleep(0.5)  # Sleeping just to make sure the response is not missed...
        await client.stop_notify(WT9011.CHAR_NOTIFY)

    async def _set_return_rate(self, client: BleakClient, rate: float):
        return_rate_to_hex = {
            0.2: 0x01,
            0.5: 0x02,
            1.0: 0x03,
            2.0: 0x04,
            5.0: 0x05,
            10.0: 0x06,
            20.0: 0x07,
            50.0: 0x08,
            100.0: 0x09,
            200.0: 0x0B,
            -1.0: 0x0C,
        }
        hex = return_rate_to_hex.get(rate, None)
        if hex is None:
            raise ValueError("Wrong return rate")

        command = bytearray([0xFF, 0xAA, 0x03, hex, 0x00])
        print(f"Setting the return rate to {'single return' if rate == -1 else str(rate) + ' Hz'}")
        await client.write_gatt_char(WT9011.CHAR_WRITE, command, response=False)

    async def run_ble_client(
        self, queue: asyncio.Queue, listen=True, battery=False, return_rate=None
    ):
        device = await self._find_device()
        print("Connecting to the device...")

        async with BleakClient(device) as client:
            print("Connected")

            if return_rate is not None:
                await self._set_return_rate(client, return_rate)

            if battery:
                await self._get_battery_level(queue, client)

            if listen:
                await self._listen_for_notifies(queue, client)

            # Send an "exit command to the consumer"
            await queue.put((time.time(), None))

        print("Disconnected")

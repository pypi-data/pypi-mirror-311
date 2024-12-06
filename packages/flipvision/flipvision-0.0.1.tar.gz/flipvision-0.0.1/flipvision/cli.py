import argparse
import asyncio

from .parser import BatteryData, InertialMeasurementData, UnknownData, WT9011Parser
from .sensor import WT9011, DeviceNotFoundError


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()

    device_group = arg_parser.add_mutually_exclusive_group()

    device_group.add_argument(
        "-n",
        "--name",
        metavar="<name>",
        default="WT901BLE67",
        help="The name of the bluetooth device to connect to",
    )

    device_group.add_argument(
        "-a",
        "--address",
        metavar="<address>",
        help="The mac address of the bluetooth device to connect to",
    )

    def valid_return_rate(value):
        allowed_values = {0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, -1}
        try:
            value = float(value)
        except ValueError:
            pass
        if value not in allowed_values:
            raise argparse.ArgumentTypeError(
                f"Invalid return rate. Allowed values are: {', '.join(map(str, allowed_values))}."
            )
        return value

    arg_parser.add_argument(
        "-r",
        "--return-rate",
        type=valid_return_rate,
        metavar="<rate>",
        help="Set the return rate in Hz. Allowed values are 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200 and -1 for single return",
    )

    arg_parser.add_argument(
        "-b",
        "--battery",
        action="store_true",
        help="Get battery level",
    )

    arg_parser.add_argument(
        "-l",
        "--listen",
        action="store_true",
        help="Listen for imu notifies",
    )

    arg_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Show unknown data frames",
    )

    return arg_parser.parse_args()


def consume(args: argparse.Namespace, data: bytearray):
    data_parser = WT9011Parser()
    types_to_parse = []

    if args.listen:
        types_to_parse.append(InertialMeasurementData)

    if args.battery:
        types_to_parse.append(BatteryData)

    if args.debug:
        types_to_parse.append(UnknownData)

    parsed_data_list = data_parser.parse(types_to_parse, data)

    for parsed in parsed_data_list:
        match parsed:
            case InertialMeasurementData():
                parsed.pretty_print()
            case BatteryData():
                print(parsed)
            case UnknownData():
                print(parsed)
                print(f"len={len(parsed.raw_data)}")
        print()


async def run_queue_consumer(args: argparse.Namespace, queue: asyncio.Queue):
    print("Starting the consumer queue")

    while True:
        # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
        epoch, data = await queue.get()
        if data is None:
            print("Exiting the consumer loop...")
            break
        else:
            consume(args, data)


async def ble_main(args: argparse.Namespace):
    queue = asyncio.Queue()

    sensor = WT9011(args.address, args.name)
    client_task = sensor.run_ble_client(queue, args.listen, args.battery, args.return_rate)
    consumer_task = run_queue_consumer(args, queue)

    try:
        await asyncio.gather(client_task, consumer_task)
    except DeviceNotFoundError:
        pass


def main():
    args = parse_args()
    asyncio.run(ble_main(args))

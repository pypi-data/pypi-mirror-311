import struct
from dataclasses import dataclass

from .sensor import WT9011


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __mul__(self, other: float):
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float):
        return Vector3(self.x / other, self.y / other, self.z / other)


@dataclass
class InertialMeasurementData:
    lin_accel: Vector3  # linear acceleration
    ang_vel: Vector3  # angular velocity
    angle: Vector3

    def pretty_print(self):
        print(
            "Linear Acceleration (m/s^2):    "
            f"   ax = {self.lin_accel.x:>8.2f}  "
            f"   ay = {self.lin_accel.y:>8.2f}  "
            f"   az = {self.lin_accel.z:>8.2f}"
        )
        print(
            "Angular Velocity (°/s):         "
            f"   wx = {self.ang_vel.x:>8.2f}  "
            f"   wy = {self.ang_vel.y:>8.2f}  "
            f"   wz = {self.ang_vel.z:>8.2f}"
        )
        print(
            "Angle (°):                      "
            f" roll = {self.angle.x:>8.2f}  "
            f"pitch = {self.angle.y:>8.2f}  "
            f"  yaw = {self.angle.z:>8.2f}"
        )


@dataclass
class BatteryData:
    voltage: float
    percentage: float


@dataclass
class UnknownData:
    raw_data: bytearray


# WT9011 Datasheet/Manual src:
# https://manuals.plus/m/65ba8c4db28ab28226fb0dc1667166259ea316332b848d51c296430336998cb2_optim.pdf
class WT9011Parser:
    def parse(self, types_to_parse: [], data: bytearray) -> []:
        parsed_data_list = []

        # Frames are 20-byte raw data packets sent by the sensor
        # The first byte is a packet header
        # and the second byte is a flag byte
        # Whole definition is in the docs (src: page 15.)
        frames = self._split_to_frames(data)
        for frame in frames:
            parsed_data = self._parse_frame(types_to_parse, frame)
            if parsed_data is not None:
                parsed_data_list.append(parsed_data)
        return parsed_data_list

    def _split_to_frames(self, data: bytearray) -> []:
        delimiter = bytearray([WT9011.PACKET_HEADER])

        # Split data array to frames
        frames = []
        # split_parts are frames without the packet packet_header
        # data.split() removes the delimiter from the array
        split_parts = data.split(delimiter)
        for part in split_parts:
            # When the delimiter is the first element of data
            # data.split() adds an b'' as a first element of split_parts
            # Skip it as it doesn't contain any data
            if part == b"":
                continue

            # Re-add the packet header to each frame
            frame = delimiter + part
            frames.append(frame)
        return frames

    def _parse_frame(self, types_to_parse: [], frame):
        if len(frame) != 20:
            return UnknownData(frame) if UnknownData in types_to_parse else None

        flag_byte = frame[1]
        match flag_byte:
            case WT9011.FLAG_INERTIAL:
                return self._parse_imu(frame) if InertialMeasurementData in types_to_parse else None
            case WT9011.FLAG_BATTERY:
                return self._parse_battery(frame) if BatteryData in types_to_parse else None
            case _:
                return UnknownData(frame) if UnknownData in types_to_parse else None

    def _parse_imu(self, frame: bytearray) -> InertialMeasurementData:
        # B- byte
        # h- short (2 bytes)
        fmt = "BBhhhhhhhhh"
        (packet_header, mark_bit, ax, ay, az, wx, wy, wz, roll, pitch, yaw) = struct.unpack(
            fmt, frame
        )

        EARTH_ACCELERATION = 9.8  # in m/s^2

        # Measurement ranges of the sensors (src: page 7.)
        ACCEL_RANGE = 16.0  # in g units
        GYRO_RANGE = 2000.0  # in degrees/s
        ANGLE_RANGE = 180.0  # in degrees

        # Used to normalize the data from sensor values to the (-1, 1) range
        # Registers are 8-bits long, two registers combined (16-bits) store a sensor value
        # 16-bit signed integers range from -32768 to 32767
        # To better understand what this variable represents see *the example below*
        SCALING_FACTOR = 32768.0

        # *the example below*
        # ax - 16 bit sensor data in range (-32768, 32767)
        # ax / SCALING_FACTOR - sensor data normalized to range (-1, 1)
        # ax / SCALING_FACTOR * ACCEL_RANGE * GRAVITY_ACCELERATION - normalized scaled to the real world units based on the sensor range
        lin_accel = Vector3(ax, ay, az) / SCALING_FACTOR * ACCEL_RANGE * EARTH_ACCELERATION

        ang_vel = Vector3(wx, wy, wz) / SCALING_FACTOR * GYRO_RANGE

        angle = Vector3(roll, pitch, yaw) / SCALING_FACTOR * ANGLE_RANGE

        return InertialMeasurementData(lin_accel, ang_vel, angle)

    def _parse_battery(self, frame: bytearray) -> BatteryData:
        MAX_VOLTAGE = 4.1
        MIN_VOLTAGE = 3.2
        voltage_raw = int.from_bytes(frame[4:6], byteorder="little")
        voltage = voltage_raw / 100.0

        def map_range(value, in_min, in_max, out_min, out_max):
            mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
            return max(out_min, min(out_max, mapped))  # Clamp to [out_min, out_max]

        percentage = map_range(voltage, MIN_VOLTAGE, MAX_VOLTAGE, 0, 100)

        return BatteryData(voltage, percentage)

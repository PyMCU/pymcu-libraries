# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Minimal I2CDevice probe in the PyMCU subset: construct over the board's I2C
# bus (probe=True, the default), then run the register write + read transaction
# every sensor/display driver on the bus makes. The upstream simpletest prints
# the result with "".join(...) in expression position, which does not compile;
# this keeps its transaction shape instead.

import board
import busio

from adafruit_bus_device.i2c_device import I2CDevice

DEVICE_ADDRESS = 0x68  # device address of DS3231 board
A_DEVICE_REGISTER = 0x0E  # device id register on the DS3231 board

comm_port = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(comm_port, DEVICE_ADDRESS)

with device as bus_device:
    bus_device.write(bytearray([A_DEVICE_REGISTER]))
    result = bytearray(1)
    bus_device.readinto(result)

print(result[0])

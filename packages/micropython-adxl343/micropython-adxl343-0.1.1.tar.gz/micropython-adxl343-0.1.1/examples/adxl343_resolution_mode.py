# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adxl343 import adxl343

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adx = adxl343.ADXL343(i2c)


adx.resolution_mode = adxl343.LOW_RES
adx.acceleration_range = adxl343.RANGE_16

while True:
    for acceleration_range in adxl343.acceleration_range_values:
        print("Current Acceleration range setting: ", adx.acceleration_range)
        for _ in range(2):
            accx, accy, accz = adx.acceleration
            print("x:{:.2f}m/s2, y:{:.2f}m/s2, z:{:.2f}m/s2".format(accx, accy, accz))
            time.sleep(0.5)
        adx.acceleration_range = acceleration_range

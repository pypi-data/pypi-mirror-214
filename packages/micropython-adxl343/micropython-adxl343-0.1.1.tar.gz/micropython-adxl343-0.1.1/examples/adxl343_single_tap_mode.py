# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adxl343 import adxl343

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adx = adxl343.ADXL343(i2c)


adx.single_tap_mode = adxl343.ST_ENABLED

adx.tap_threshold = 4  # m/s2
adx.tap_duration = 625  # us

while True:
    print(f"Single Tap detected {adx.single_tap_activated}")
    time.sleep(0.5)

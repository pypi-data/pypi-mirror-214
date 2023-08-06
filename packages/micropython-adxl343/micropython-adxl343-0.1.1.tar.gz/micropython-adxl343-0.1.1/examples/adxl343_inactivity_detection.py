# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adxl343 import adxl343

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adx = adxl343.ADXL343(i2c)


adx.inactivity_threshold = 20  # m/s2
adx.inactivity_mode = adxl343.INACTIVITY_ENABLED
adx.inactivity_duration = 3

while True:
    print(f"Inactivity detected {adx.inactivity_detected}")
    time.sleep(0.5)

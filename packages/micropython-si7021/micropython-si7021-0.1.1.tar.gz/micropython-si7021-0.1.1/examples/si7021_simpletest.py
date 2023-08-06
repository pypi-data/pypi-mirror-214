# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
import si7021

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
si = si7021.SI7021(i2c)

while True:
    print("Temperature: ", si.temperature)
    print("Humidity: ", si.humidity)
    time.sleep(1)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

from time import sleep
from machine import Pin, I2C, ADC
from micropython_ds1841 import ds1841

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
ds1841 = ds1841.DS1841(i2c)

wiper_output = ADC(Pin(26, mode=Pin.IN))

while True:
    # set th
    ds1841.wiper = 127
    print("Wiper set to %d" % ds1841.wiper)
    voltage = wiper_output.read_u16()
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

    ds1841.wiper = 0
    print("Wiper set to %d" % ds1841.wiper)
    voltage = wiper_output.read_u16()
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

    ds1841.wiper = 63
    print("Wiper set to %d" % ds1841.wiper)
    voltage = wiper_output.read_u16()
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

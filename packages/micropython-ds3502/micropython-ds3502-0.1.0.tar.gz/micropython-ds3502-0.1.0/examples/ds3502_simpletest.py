# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya#
#
# SPDX-License-Identifier: MIT

from time import sleep
from machine import Pin, I2C, ADC
from micropython_ds3502 import ds3502

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
ds3502 = ds3502.DS3502(i2c)

wiper_output = ADC(Pin(26, mode=Pin.IN))

while True:
    # set th
    ds3502.wiper = 127
    print("Wiper set to %d" % ds3502.wiper)
    voltage = wiper_output.read_u16()
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

    ds3502.wiper = 0
    print("Wiper set to %d" % ds3502.wiper)
    voltage = wiper_output.read_u16()
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

    ds3502.wiper = 63
    print("Wiper set to %d" % ds3502.wiper)
    voltage = wiper_output.read_u16()
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

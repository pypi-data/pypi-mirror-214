# SPDX-FileCopyrightText: 2019 Bryan Siepert for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`ds3502`
================================================================================

MicroPython Driver for the DS3502 Potentiometer

All Code adapted for Micropython from:
https://github.com/adafruit/Adafruit_CircuitPython_DS3502


* Author(s): Bryan Siepert, Jose D. Montoya


"""

from time import sleep
from micropython import const
from micropython_ds3502.i2c_helpers import CBits, RegisterStruct


__version__ = "0.1.1"
__repo__ = "https://github.com/jposada202020/MicroPython_DS3502.git"

_REG_WIPER = const(0x00)  # Wiper value register (R/W)
_REG_CONTROL = const(0x02)  # Configuration Register (R/W)


class DS3502:
    """Driver for the DS3502 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the DS3502 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x28`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`DS3502` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        import ds3502

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(sda=Pin28), scl=Pin(3))
        ds3502 = ds3502.DS3502(i2c)


    """

    _wiper = RegisterStruct(_REG_WIPER, ">B")
    _write_only_to_wiper = CBits(1, _REG_CONTROL, 7)

    def __init__(self, i2c, address: int = 0x28) -> None:
        self._i2c = i2c
        self._address = address
        self._write_only_to_wiper = True

    @property
    def wiper(self) -> int:
        """
        Potentiometer's wiper value
        """
        return self._wiper

    @wiper.setter
    def wiper(self, value: int) -> None:
        if value < 0 or value > 127:
            raise ValueError("wiper must be from 0-127")
        self._wiper = value

    def set_default(self, default: int) -> None:
        """Sets the wiper's default value and current value to the given value

        :param int default: The value from 0-127 to set as the wiper's default.
        """
        self._write_only_to_wiper = False
        self.wiper = default
        sleep(0.1)  # wait for write to eeprom to finish
        self._write_only_to_wiper = True

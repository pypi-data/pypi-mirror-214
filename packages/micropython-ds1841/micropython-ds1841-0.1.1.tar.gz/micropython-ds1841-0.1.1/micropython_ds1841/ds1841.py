# SPDX-FileCopyrightText: 2020 Bryan Siepert for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`ds1841`
================================================================================

MicroPython Driver for the DS1841 Potentiometer

All code from

Adapted for Micropython


* Author(s): Bryan Siepert, Jose D. Montoya


"""

from time import sleep
from micropython import const
from micropython_ds1841.i2c_helpers import CBits, RegisterStruct


__version__ = "0.1.1"
__repo__ = "https://github.com/jposada202020/MicroPython_DS1841.git"

_IVR = const(0x00)
_CR0 = const(0x02)
_CR1 = const(0x03)
_LUTAR = const(0x08)
_WR = const(0x09)
_CR2 = const(0x0A)
_TEMP = const(0x0C)
_VOLTAGE = const(0x0E)
_LUT = const(0x80)

_VCC_LSB = const(25.6)


class DS1841:
    """Driver for the DS1841 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the DS1841 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x28`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`DS1841` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        import ds1841

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(sda=Pin28), scl=Pin(3))
        ds1841 = ds1841.DS1841(i2c)

    """

    _lut_address = RegisterStruct(_LUTAR, ">B")
    _wiper_register = RegisterStruct(_WR, ">B")

    _temperature_register = RegisterStruct(_TEMP, ">b")
    _voltage_register = RegisterStruct(_VOLTAGE, ">B")

    _disable_save_to_eeprom = CBits(1, _CR0, 7)

    _initial_value_register = RegisterStruct(_IVR, ">B")
    _adder_mode_bit = CBits(1, _CR1, 1)
    _update_mode = CBits(1, _CR1, 0)

    _manual_lut_address = CBits(1, _CR2, 1)
    _manual_wiper_value = CBits(1, _CR2, 2)

    def __init__(self, i2c, address: int = 0x28) -> None:
        self._i2c = i2c
        self._address = address

        self._disable_save_to_eeprom = True
        self._adder_mode_bit = False

        self._manual_lut_address = True
        self._manual_wiper_value = True
        self._lut_mode_enabled = False
        self._update_mode = True

    @property
    def wiper(self) -> int:
        """The value of the potentionmeter's wiper.
        :param wiper_value: The value from 0-127 to set the wiper to.
        """
        return self._wiper_register

    @wiper.setter
    def wiper(self, value: int) -> None:
        if value > 127:
            raise AttributeError("wiper must be from 0-127")
        self._wiper_register = value

    @property
    def wiper_default(self) -> int:
        """Sets the wiper's default value and current value to the given value
        :param new_default: The value from 0-127 to set as the wiper's default.
        """

        return self._initial_value_register

    @wiper_default.setter
    def wiper_default(self, value: int) -> None:
        if value > 127:
            raise AttributeError("initial_value must be from 0-127")
        self._disable_save_to_eeprom = False
        self._update_mode = False
        sleep(0.2)
        self._initial_value_register = value
        sleep(0.2)
        self._disable_save_to_eeprom = True
        self._update_mode = True

    @property
    def temperature(self) -> int:
        """The current temperature in degrees celsius"""
        return self._temperature_register

    @property
    def voltage(self) -> float:
        """The current voltage between VCC and GND"""
        return self._voltage_register * _VCC_LSB

    @property
    def lut_mode_enabled(self) -> bool:
        """Enables LUT mode. LUT mode takes sets the value of the Wiper based on the entry in a
        72-entry Look Up Table. The LUT entry is selected using the `lut_selection`
        property to set an index from 0-71
        """
        return self._lut_mode_enabled

    @lut_mode_enabled.setter
    def lut_mode_enabled(self, value: bool) -> None:
        self._manual_lut_address = value
        self._update_mode = True
        self._manual_wiper_value = not value
        self._lut_mode_enabled = value

    @property
    def lut_selection(self) -> int:
        """Choose the entry in the Look Up Table to use to set the wiper.
        :param index: The index of the entry to use, from 0-71.
        """
        if not self._lut_mode_enabled:
            raise RuntimeError(
                "lut_mode_enabled must be equal to True to use lut_selection"
            )
        return self._lut_address - _LUT

    @lut_selection.setter
    def lut_selection(self, value: int) -> None:
        if value > 71 or value < 0:
            raise IndexError("lut_selection value must be from 0-71")
        self._lut_address = value + _LUT
        sleep(0.020)

"""
---
(c) 2022 David SPORN
---
This is part of Sporniket's "The Pretender -- Atari STe" project.

Sporniket's "The Pretender -- Atari STe" project is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Sporniket's "The Pretender -- Atari STe" project is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Sporniket's "The Pretender -- Atari STe" project.
If not, see <https://www.gnu.org/licenses/>. 
---
"""
### builtin deps
from enum import Enum
from typing import List  # , Dict, Tuple, Optional

### amaranth -- main deps
from amaranth import *
from amaranth.build import Platform


class SelectedSubsystem(Enum):
    NONE = 0
    ROM = 1
    RAM = 2
    ROM_CARTRIDGE = 4


class AddressDecoder24Bits(Elaboratable):
    def __init__(self):
        self.address_page = Signal(4)
        self.address_sub_page = Signal(4)
        self.address_sub_sub_page = Signal(8)
        self.address_long = Signal(6)
        self.fc = Signal(3)
        self.rxw = Signal()
        self.decode = Signal(2, reset=SelectedSubsystem.ROM.value)
        self.error = Signal()

    def ports(self) -> List[Signal]:
        return [
            self.address_page,
            self.address_sub_page,
            self.address_sub_sub_page,
            self.address_long,
            self.fc,
            self.rxw,
            self.decode,
            self.error,
        ]

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        # reset error state, unless there is match below
        m.d.sync += self.error.eq(1)
        # reset selection state, unless there is a match below
        m.d.sync += self.decode.eq(SelectedSubsystem.NONE.value)

        with m.If(((self.fc)[2])):
            # super user mode
            with m.If(((self.address_page) == 0)):
                self.elaborate_super_page0(m, platform)
        with m.If((~(self.fc)[2])):
            # user mode
            with m.If(((self.address_page) == 0)):
                self.elaborate_user_page0(m, platform)
        return m

    def elaborate_super_page0(self, m: Module, platform: Platform):
        m.d.sync += [
            self.decode.eq(SelectedSubsystem.RAM.value),
            self.error.eq(0),
        ]  # select RAM by default
        with m.If(
            ((self.address_sub_page) == 0)
            & ((self.address_sub_sub_page) == 0)
            & ((self.address_long == 0) | (self.address_long == 1))
        ):
            m.d.sync += [self.decode.eq(SelectedSubsystem.ROM.value)]

    def elaborate_user_page0(self, m: Module, platform: Platform):
        m.d.sync += [
            self.decode.eq(SelectedSubsystem.RAM.value),
            self.error.eq(0),
        ]  # select RAM by default
        with m.If(
            ((self.address_sub_page) == 0)
            & ((self.address_sub_sub_page) == 0)
            & ((self.address_long == 0) | (self.address_long < 200))
        ):
            # prevent any access under address 0x800
            m.d.sync += [self.decode.eq(SelectedSubsystem.NONE.value), self.error.eq(1)]

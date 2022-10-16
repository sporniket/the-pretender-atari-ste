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
from typing import List  # , Dict, Tuple, Optional

### amaranth -- main deps
from amaranth import *
from amaranth.build import Platform

### amaranth -- test deps
from amaranth.asserts import *  # AnyConst, AnySeq, Assert, Assume, Cover, Past, Stable, Rose, Fell, Initial

### amaranth-stuff -- deps
from amaranth_stuff.testing import Test

### the pretender atari ste -- deps
from pretender.atari_ste import AddressDecoder24Bits, SelectedSubsystem


def test_shouldDecodePage0_theTwoFirstLongAreMappedToROM():
    def testBody(m: Module, cd: ClockDomain):
        rst = cd.rst
        decoder = m.submodules.dut
        for i in (0, 1):
            with m.If(
                ~Past(rst)
                & (Past(decoder.fc)[2])
                & (Past(decoder.address_page) == 0)
                & (Past(decoder.address_sub_page) == 0)
                & (Past(decoder.address_sub_sub_page) == 0)
                & Past(decoder.address_long)
                == i
            ):
                m.d.sync += [
                    Assert(decoder.decode == SelectedSubsystem.ROM.value),
                    Assert(~(decoder.error)),
                ]

    Test.describe(
        "should Decode Page0 -- the Two First Long Are Mapped To ROM",
        AddressDecoder24Bits(),
        testBody,
        2,
    )


def test_shouldDecodePage0_theRamIsMappedStartingFromThirdLong():
    def testBody(m: Module, cd: ClockDomain):
        rst = cd.rst
        decoder = m.submodules.dut
        with m.If(
            ~Past(rst)
            & (Past(decoder.fc)[2])
            & (Past(decoder.address_page) == 0)
            & (Past(decoder.address_sub_page) == 0)
            & (Past(decoder.address_sub_sub_page) == 0)
            & Past(decoder.address_long)
            > 1
        ):
            m.d.sync += [
                Assert(decoder.decode == SelectedSubsystem.RAM.value),
                Assert(~(decoder.error)),
            ]
        with m.If(
            ~Past(rst)
            & (Past(decoder.fc)[2])
            & (Past(decoder.address_page) == 0)
            & (Past(decoder.address_sub_page) == 0)
            & (Past(decoder.address_sub_sub_page) > 0)
        ):
            m.d.sync += [
                Assert(decoder.decode == SelectedSubsystem.RAM.value),
                Assert(~(decoder.error)),
            ]
        with m.If(
            ~Past(rst)
            & (Past(decoder.fc)[2])
            & (Past(decoder.address_page) == 0)
            & (Past(decoder.address_sub_page) > 0)
        ):
            m.d.sync += [
                Assert(decoder.decode == SelectedSubsystem.RAM.value),
                Assert(~(decoder.error)),
            ]

    Test.describe(
        "should Decode Page0 -- the RAM Is Mapped Starting From Third Long",
        AddressDecoder24Bits(),
        testBody,
        2,
    )

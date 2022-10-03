> This is a slow project, don't hold your breath to see it completed.

# The pretender 'Atari STe'

> The 'Atari STe' is : 
> * a computer produced around 1989 by a US company known as 'Atari'
> * a member of a family of computers made by said company, denoted "Atari ST", "ST" meaning "Sixty-Thirty-two" (16/32) after the data bus architecture of the main processor (a physical data bus of 16 bits, data registers of 32 bits)
> * a computer designed for a CPU made by a manufacturer that was known as 'Motorola' during the 1970-1990 period : the MC68000


## What is it ?

This is an FPGA project that intends to implement the memory map, or in other words the hardware registers, of the computer known as 'Atari STe'. The goal being to connect the FPGA board to a real MC68000 on one side, and have a screen, keyboard, mouse and joysticks on the other side, and the end result works close enough to a real STe with a standard ROM (TOS 1.6x, TOS 2.0x) as well as EmuTOS feel like being on a STe. If some GEM applications, and even some games, are able to run on this, that would be good. 

## What is it not ?

This project WILL NOT be another faithfull recreation of each chip found inside an Atari STe (especially the customs chips known as GSTMCU/Combel, the Shifter, the Blitter and the DMA). For that, a lot of project already exists (for MyST ; for MySTer FPGA ; the Suska project ; and surely others)

As implied by the name of the project, it aims to "pretend" that this is an Atari STe, by implementing the behavior of known hardware registers. 

E.g. when the Shifter hardware register video mode is `0x00`, then the RAM area used to store the framebuffer is read as a 4 interleaved bitplans to render a 320x200pixels screen with borders, using the 16 RGB-444 colors defined in the 16 16bits registers of the Shifter storing the palette. And if the pretend is advanced enough, it could also infers that when some writes in the hardware register storing the video vertical frequency (50/60/70Hz) happens at some critical moment, it should extends the rendering beyond the respective borders. This late behaviour implementation would be a courtesy to legacy software, but it will not go into much details (meaning : the timing constraints to open a border will be quite relaxed compared to real hardware).

## For which FPGA/Hardware ?

I will start working using the ['ColorLight i9'](https://github.com/wuxx/Colorlight-FPGA-Projects/blob/master/colorlight_i9_v7.2.md), a board powered by an ECP5 from Lattice with a development pcb providing an HDMI connector and almost 100 GPIOs nicely accessible ; I will be using the [amaranth-hdl](https://github.com/amaranth-lang/amaranth/) python library and all the opensource toolchain found in the [OSS-CAD-Suite](https://github.com/YosysHQ/oss-cad-suite-build)

I will use a real MC68HC000 cpu. This HC version is able to run at 3.3 volts instead of 5. To enforce the aspect of "not a faithfull recreation at all", this CPU will be clocked at 27MHz/4 = 6.75MHz at first, then 27MHz/2 = 13.5MHz, then hopefully at 27MHz. 27MHz is the pixel clock for Simple Definition TV at 50Hz over HDMI.

The hardware part of this project will consist in a PCB holding the CPU (at 3.3v). 

The PCB will also provide 5v or 3.3v ports, in order to have : 
* a cartridge port, mainly to run a diagnostic cartridge (5V)
* a SPI channel connected to a SD card reader (3.3v) to emulate floppies and ACSI hard drives
* 3 serial ports (each ports is a pair TX/RX), accessible both at 3.3v and 5v meaning each port is broke out into 4 pins.
  * one for the RS-232 port
  * one for IKBD
  * one for the MIDI
* Some way to display some meta information/debug bits : some LEDs and an OLED display, surely through an I2C expander


That's all for now, until next time.


# Lessons

All my lessons, in the order I did them. They aren't owned by one section: each lesson pulls from whatever topic it needs, and most of them feed more than one part of my work. The section pages ([radar](../radar/), [DCA1000 removal](../dca1000-removal/), [FPGA and acceleration](../fpga-acceleration/)) summarize what these lessons taught me for that area.

| # | Lesson | Feeds |
|---|---|---|
| 1 | [The FPGA mental model](01-fpga-mental-model.md): PS vs PL, AXI-Lite vs AXI-Stream, DMA | FPGA · DCA1000 |
| 2 | [Signals, the FFT, and FMCW radar](02-signals-fft-fmcw.md): I/Q samples, FFT, chirp → beat frequency, range resolution | Radar · FPGA |
| 3 | [Break the radar on purpose](03-fft-experiments.md): aliasing, resolution vs. FFT size | Radar · FPGA |
| 4 | [Numbers in hardware (fixed point)](04-fixed-point.md): two's complement, Q1.15, FFT overflow, packing samples | FPGA · DCA1000 · Radar |
| K1 | [LVDS](K1-lvds.md): differential signalling, termination, the radar's lanes, DDR clock | DCA1000 · Radar · FPGA |
| K2 | [Serial protocols](K2-serial-protocols.md): UART, SPI, I²C, source-synchronous LVDS | DCA1000 · FPGA |
| K3 | [Flip-flops, counters, shift registers](K3-flipflops-counters-shift.md) | FPGA · DCA1000 |
| K4 | [Verilog](K4-verilog-counter.md): modules, `reg`, `always`, `assign`, `if`/`else`; a serial transmitter and receiver; my mistakes writing `loopback.v` | FPGA · DCA1000 |
| K5 | [The serial link in simulation](K5-serial-link-sim.md): testbench, bit alignment, mid-bit sampling, state machines, the AXI-Stream handshake | DCA1000 · FPGA |
| K7b | [Pins from Python (AXI GPIO)](K7b-axi-gpio-python.md): DATA/TRI registers, write mask, reading a pin, sending a byte, 13.7 µs per write | DCA1000 · FPGA |

Hands-on work (lab guides, code, photos) lives in the section where it was done, e.g. [lab day 1](../dca1000-removal/LAB-DAY-1-LAPTOP.md). The full lesson plan is [here](../dca1000-removal/PLAN.md).

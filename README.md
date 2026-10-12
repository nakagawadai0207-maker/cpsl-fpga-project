# cpsl-fpga-project

I am an undergraduate research assistant at Duke University's Cyber-Physical Systems Lab (CPSL). This is my journey through learning FPGA basics and how they apply to radar.

**The goal:** learn how an FPGA (AMD Kria KR260 / K26) can speed up FMCW mmWave radar processing. I'm starting from zero, and I want skills that also carry over to chip design and quantum-control hardware.

## Layout

| Path | What's in it |
|---|---|
| [PROGRESS.md](PROGRESS.md) | Progress bars + dated log |
| [notes/](notes/) | One file per lesson: what I learned, in my own words, plus check questions I got wrong and why |
| [kria-link/](kria-link/) | Sub-project: two Krias talking over LVDS ([plan](kria-link/PLAN.md)) |
| [code/](code/) | Scripts I wrote or ran for the lessons |

## The path

1. **Big picture.** What an FPGA is, the PS/PL split on a Zynq, and how data moves (AXI, DMA).
2. **Signals and radar.** Complex numbers, the FFT, and FMCW chirps (beat frequency ∝ distance).
3. **Numbers in hardware.** Fixed point.
4. **Digital logic + HDL.** Harris & Harris, *Digital Design and Computer Architecture*, plus HDLBits.
5. **HLS** (hardware from C++), then the whole system on the board.
6. **Capstones**, e.g. an FFT/backprojection kernel, sizing, a bit-width study, and an LVDS deserializer sim.

Lab-internal code and documents are kept out of this repo.

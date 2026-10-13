# FPGA and hardware acceleration

**Goal (for my future):** learn
1. **How an FPGA fits into a whole system:** pins → custom logic (PL) → a standard bus (AXI) → memory → a processor running software (PS). Almost every FPGA product has this shape, including quantum control hardware and chip test setups.
2. **How to hardware-accelerate a computation:** memory → DMA → my logic → DMA → memory, started and read from software, and measured against Python to check it's worth it.

## Notes
- [Lesson 1: the FPGA mental model](notes/01-fpga-mental-model.md): PS vs PL, AXI-Lite vs AXI-Stream, DMA
- [Lesson 4: numbers in hardware (fixed point)](notes/04-fixed-point.md): two's complement, Q1.15, FFT overflow and scaling

## FPGA basics learned inside the DCA1000 work
These lessons live in [dca1000-removal/](../dca1000-removal/) because that's where I needed them:
- [K3: flip-flops, counters, shift registers](../dca1000-removal/K3-flipflops-counters-shift.md)
- [K4: Verilog](../dca1000-removal/K4-verilog-counter.md)
- The Vivado tool flow (block design, constraints, bitstream, loading it): [lab day 1](../dca1000-removal/LAB-DAY-1-LAPTOP.md)
- Coming up in the [plan](../dca1000-removal/PLAN.md): **K7b** (software controls my logic through AXI GPIO), **K10** (AXI-Stream + DMA into memory), **K12** (my first hardware accelerator: an FFT in the DMA loop, timed against NumPy)

## The longer path (main lesson plan, mostly paused)
1. Big picture: what an FPGA is, PS/PL, how data moves (AXI, DMA). ✓
2. Signals and radar (see [radar/](../radar/)). ✓
3. Numbers in hardware: fixed point. ✓
4. Digital logic + HDL: Harris & Harris, *Digital Design and Computer Architecture*, plus HDLBits (paused; needed sections pulled into K3–K4)
5. HLS (hardware from C++), then the whole system on the board
6. Capstones: an FFT/backprojection kernel, sizing (does it fit on the chip?), a bit-width study, an LVDS deserializer sim

# FPGA and hardware acceleration

**Goal (for my future):** learn
1. **How an FPGA fits into a whole system:** pins → custom logic (PL) → a standard bus (AXI) → memory → a processor running software (PS). Almost every FPGA product has this shape, including quantum control hardware and chip test setups.
2. **How to hardware-accelerate a computation:** memory → DMA → my logic → DMA → memory, started and read from software, and measured against Python to check it's worth it.

## What I've learned
- **PS and PL:** the Kria chip is ARM cores running Linux (PS) plus FPGA fabric (PL), connected by AXI buses; DMA moves data without the CPU touching each word. ([Lesson 1](../lessons/01-fpga-mental-model.md))
- **Hardware does math in integers:** two's complement, Q1.15 fixed point, and why an FFT in hardware must scale to avoid overflow. ([Lesson 4](../lessons/04-fixed-point.md))
- **The FFT** is the first computation worth accelerating, and FFT size sets its cost. ([Lessons 2](../lessons/02-signals-fft-fmcw.md) and [3](../lessons/03-fft-experiments.md))
- **Building blocks of all digital logic:** flip-flops, counters, shift registers. ([K3](../lessons/K3-flipflops-counters-shift.md))
- **Writing hardware in Verilog** and getting it onto a real chip: block design, constraints, bitstream, `xmutil`. ([K4](../lessons/K4-verilog-counter.md), [lab day 1](../dca1000-removal/LAB-DAY-1-LAPTOP.md))
- **I/O standards and pin banks:** what a pin can do depends on its bank. ([K1](../lessons/K1-lvds.md))

## Coming up
From the [plan](../dca1000-removal/PLAN.md): **K7b** (software controls my logic through AXI GPIO), **K10** (AXI-Stream + DMA into memory), **K12** (my first hardware accelerator: an FFT in the DMA loop, timed against NumPy). After that, the paused capstones: a backprojection kernel, sizing (does it fit on the chip?), a bit-width study, and HLS (hardware from C++).

# Radar

**Goal:** understand how the lab's FMCW mmWave radar turns reflections into distances, well enough to follow the lab's research and to know what the FPGA work has to process.

## What I've learned
- A chirp's echo, mixed with the outgoing chirp, gives a **beat frequency proportional to distance**; the FFT turns that into a range profile. ([Lesson 2](../lessons/02-signals-fft-fmcw.md))
- Samples are **complex (I/Q)**; **range resolution** is set by the chirp's bandwidth. ([Lesson 2](../lessons/02-signals-fft-fmcw.md))
- Targets past the maximum range **alias** (a 4.5 m target shows up at 0.57 m), and FFT size trades resolution against cost. ([Lesson 3](../lessons/03-fft-experiments.md), [script](code/lesson3.py))
- The ADC's samples are 14-bit values stored in 16-bit slots. ([Lesson 4](../lessons/04-fixed-point.md))
- The radar chip sends its raw samples out over **LVDS**: data lanes, a DDR bit clock and a frame clock. ([K1](../lessons/K1-lvds.md))

## Reading
- TI, *Introduction to mmWave Sensing: FMCW Radars* (Sandeep Rao): slide deck, in progress

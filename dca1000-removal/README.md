# DCA1000 removal

**Goal (my main contribution to the lab):** today the chain is radar → DCA1000 capture board → Ethernet → PC. The goal is radar → Kria: the Kria's FPGA receives the radar's LVDS data itself, rebuilds the samples, puts them in memory and configures the radar, which is everything the DCA1000 does now.

**First step:** get two Kria boards talking over a serial link (single-ended on the KR260's 3.3 V PMOD pins first, true LVDS later), shown by one board lighting an LED on the other. I'm helping a labmate with this.

## What I've learned for this
- **LVDS:** the receiver reads the difference between two wires, which cancels noise; it needs 100 Ω termination. 3.3 V PMOD pins (HD banks) can't transmit LVDS. ([K1](../lessons/K1-lvds.md))
- **Every serial link** has to solve when to read each bit and where a word starts; the radar sends a clock and a frame signal for that. ([K2](../lessons/K2-serial-protocols.md))
- **A serial receiver** is a shift register plus a counter. ([K3](../lessons/K3-flipflops-counters-shift.md), [K4](../lessons/K4-verilog-counter.md))
- **Samples into memory** go through AXI and DMA between the FPGA (PL) and processor (PS). ([Lesson 1](../lessons/01-fpga-mental-model.md))
- **Sample format:** how two 16-bit I/Q values pack into one 32-bit word. ([Lesson 4](../lessons/04-fixed-point.md))
- **On the real board:** the full Vivado flow, loading with `xmutil`, and a loopback test through two PMOD pins. ([lab day 1](LAB-DAY-1-LAPTOP.md))

## Plan and lab work
- [**PLAN.md**](PLAN.md): the full lesson plan, K1–K12, and why each step matters
- [Lab day 1, laptop + `xmutil` version](LAB-DAY-1-LAPTOP.md): what actually worked on 2026-10-13
- [Lab day 1, original PYNQ version](LAB-DAY-1.md)
- Code: [`loopback.v`](code/loopback.v) (written by hand), [`blink.v`](code/blink.v), [board files for `xmutil`](code/firmware/)
- [Photo of the first wiring](photos/2026-10-13-first-wiring.jpg)

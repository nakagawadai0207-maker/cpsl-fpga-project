# DCA1000 removal

**Goal (my main contribution to the lab):** today the chain is radar → DCA1000 capture board → Ethernet → PC. The goal is radar → Kria: the Kria's FPGA receives the radar's LVDS data itself, rebuilds the samples, puts them in memory and configures the radar, which is everything the DCA1000 does now.

**First step:** get two Kria boards talking over a serial link (single-ended on the KR260's 3.3 V PMOD pins first, true LVDS later), shown by one board lighting an LED on the other. I'm helping a labmate with this.

## Plan and lessons
- [**PLAN.md**](PLAN.md): the full lesson plan, K1–K12, and why each step matters
- [K1: LVDS](K1-lvds.md)
- [K2: serial protocols](K2-serial-protocols.md)
- [K3: flip-flops, counters, shift registers](K3-flipflops-counters-shift.md)
- [K4: Verilog](K4-verilog-counter.md)

## Lab work
- [Lab day 1, laptop + `xmutil` version](LAB-DAY-1-LAPTOP.md): what actually worked on 2026-10-13
- [Lab day 1, original PYNQ version](LAB-DAY-1.md)
- Code: [`loopback.v`](code/loopback.v) (written by hand), [`blink.v`](code/blink.v), [board files for `xmutil`](code/firmware/)
- [Photo of the first wiring](photos/2026-10-13-first-wiring.jpg)

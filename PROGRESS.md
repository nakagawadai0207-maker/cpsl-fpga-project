# Progress

## Where I am

| Track | Progress | |
|---|---|---|
| **FPGA lessons, overall** | `█████░░░░░░░░░░░░` | 5 / 17 |
| A: Foundations (L0–L7, L5b, L5c) | `█████░░░░░` | 5 / 10 |
| B: Capstones (L11–L14) | `░░░░` | 0 / 4 |
| C: On the real board (L8–L10) | `░░░` | 0 / 3 |
| **Ready for the lab** (K1, K2, K3, K4 counter, Vivado ready on lab PC or laptop, parts ✓ lab has them) | `██████` | 6 / 6 ✓ |
| **Kria-to-Kria link (K1–K11)**, [plan](kria-link/PLAN.md) | `███░░░░░░░░` | 3 / 11, current focus |
| **Harris & Harris ch 1–4** (needed before Lesson 5) | `░░░░` | paused; the needed sections are pulled into K3–K4 |

Done: L0 setup · L1 FPGA mental model · L2 radar math · L3 FFT experiments · L4 fixed point
Kria link done: [K1 LVDS](kria-link/K1-lvds.md) · [K2 serial protocols](kria-link/K2-serial-protocols.md) · [K3 flip-flops, counters, shift registers](kria-link/K3-flipflops-counters-shift.md) · [K4 part 1: Verilog counter](kria-link/K4-verilog-counter.md)
Now: **Kria-to-Kria link** sub-project (two boards talking over LVDS, LED on). Main lessons and full H&H paused.

## Log

| Date | What happened |
|---|---|
| 2026-10-03 | learncpp.com chapters 0–6 + O (bit manipulation) done |
| 2026-10-09 | Got the FPGA assignment. Set up SSH/GitLab, cloned the lab repos |
| 2026-10-09 | **Lesson 0 done:** Python + NumPy installed; lab radar-processing checks pass (11/11); lab project test suite passes (65 tests) |
| 2026-10-09 | **Lesson 1 done:** FPGA mental model (PS/PL, AXI-Lite vs AXI-Stream, DMA) |
| 2026-10-09 → 10-11 | **Lesson 2 done:** complex numbers, the FFT as a tuning dial, FMCW chirp → beat frequency, range resolution |
| 2026-10-11 | **Lesson 3 done:** aliasing (4.5 m target shows at 0.57 m), resolution vs. FFT size, choosing an FFT size. Learned to run Python scripts from PowerShell |
| 2026-10-11 | **Lesson 4 done:** two's complement, Q1.15 fixed point, FFT overflow and scaling, packing complex samples, MSB-aligned ADC samples |
| 2026-10-11 | Started Harris & Harris ch 1 |
| 2026-10-12 | Started the Kria-to-Kria link sub-project (helping a labmate replace the DCA1000 capture board). Paused full H&H read-through. |
| 2026-10-12 | **K1 done:** LVDS (P − N, noise cancelling, 100 Ω termination, the radar's 4 pairs, DDR clock, bit alignment) |
| 2026-10-12 | **K2 done:** serial protocols (timing vs framing; UART, SPI, I²C, source-synchronous LVDS) |
| 2026-10-12 | **K3 done:** flip-flops, counters (LED blink math), shift registers (serial receiver = shift register + counter) |
| 2026-10-12 | **K4 part 1 done:** Verilog module/ports, reg, always/<=, assign. Wrote the loopback design's assign lines. Ready for the lab: 5/6 |
| 2026-10-13 | **First lab visit:** logged into the KR260 over USB serial and SSH (wired Ethernet only). Board runs stock Ubuntu 22.04, no PYNQ, but has `xmutil`/`fpgautil` to load designs. No lab PC, so installing Vivado 2025.2 ML Standard on my laptop. |
| 2026-10-13 | **Vivado 2025.2 installed on laptop.** Ready for the lab: 6/6 |
| 2026-10-13 | **First wiring on the KR260:** checked PMOD4 pin 11 = +3.33 V vs pin 9 with a Fluke 289, lit the LED straight from 3.3 V, then wired the loopback (pin 1 → 330 Ω → LED → pin 9, jumper pin 3 → pin 7). [Photo](photos/2026-10-13-first-wiring.jpg) |
| 2026-10-13 | **First design running on the FPGA (K7 blink, done early):** wrote `loopback.v` by hand, built it in Vivado on my laptop (Zynq block + my module, `pins.xdc`), made `dai_loopback.bit.bin`, copied it to the board with `scp` and loaded it with `xmutil loadapp`. LED blinks through the pin 3 → pin 7 jumper; pulling the jumper out of pin 7 turns it off (pulldown), plugging it back in resumes the blink. |

## Up next
- Finish K4 part 2 (receiver) and K5
- Ask Person B which Vivado version she uses
- Verilog basics (H&H ch 1–2 + HDLBits), then Lesson 5: the AXI-Stream handshake
- Harris & Harris ch 1 + HDLBits (running in parallel)

# Progress

## Where I am

| Track | Progress | |
|---|---|---|
| **FPGA lessons, overall** | `█████░░░░░░░░░░░░` | 5 / 17 |
| A: Foundations (L0–L7, L5b, L5c) | `█████░░░░░` | 5 / 10 |
| B: Capstones (L11–L14) | `░░░░` | 0 / 4 |
| C: On the real board (L8–L10) | `░░░` | 0 / 3 |
| **Harris & Harris ch 1–4** (needed before Lesson 5) | `░░░░` | 0 / 4, ch 1 in progress |

Done: L0 setup · L1 FPGA mental model · L2 radar math · L3 FFT experiments · L4 fixed point
Next: H&H ch 1 → ch 2 + HDLBits basics → Lesson 5 (AXI-Stream handshake in Verilog)

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

## Up next
- Verilog basics (H&H ch 1–2 + HDLBits), then Lesson 5: the AXI-Stream handshake
- Harris & Harris ch 1 + HDLBits (running in parallel)

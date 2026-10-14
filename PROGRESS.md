# Progress

## Where I am

### Radar ([section](radar/))
| Track | Progress | |
|---|---|---|
| Radar lessons (L2 signals/FFT/FMCW, L3 FFT experiments) | `██` | 2 / 2 ✓ |
| TI *Intro to mmWave Sensing* deck | `██░░░░░░░░` | slides 1–16 of 70 read (as of 2026-10-09) |

### DCA1000 removal ([section](dca1000-removal/)), main focus
| Track | Progress | |
|---|---|---|
| Kria link lessons (K1–K11 + K7b), [plan](dca1000-removal/PLAN.md) | `████░░░░░░░░` | 4 / 12: K1, K2, K3, K7 done; K4 half done |
| Lab setup (board login, Vivado on laptop, wiring, first bitstream, PYNQ) | `█████` | 5 / 5 ✓ |

Done: [K1 LVDS](lessons/K1-lvds.md) · [K2 serial protocols](lessons/K2-serial-protocols.md) · [K3 flip-flops, counters, shift registers](lessons/K3-flipflops-counters-shift.md) · [K4 part 1: Verilog](lessons/K4-verilog-counter.md) · K7 first design on the board ([lab guide](dca1000-removal/LAB-DAY-1-LAPTOP.md))

### FPGA and hardware acceleration ([section](fpga-acceleration/))
| Track | Progress | |
|---|---|---|
| Main FPGA lesson plan (L0–L14; L2–L3 are the radar lessons above) | `█████░░░░░░░░░░░░` | 5 / 17, paused behind the DCA1000 work |
| K12 first hardware accelerator | `░` | 0 / 1 |
| Harris & Harris ch 1–4 | `░░░░` | paused; needed sections pulled into K3–K4 |

## Log

| Date | Section | What happened |
|---|---|---|
| 2026-10-03 | Other | learncpp.com chapters 0–6 + O (bit manipulation) done |
| 2026-10-09 | Setup | Got the FPGA assignment. Set up SSH/GitLab, cloned the lab repos |
| 2026-10-09 | Setup | **Lesson 0 done:** Python + NumPy installed; lab radar-processing checks pass (11/11); lab project test suite passes (65 tests) |
| 2026-10-09 | FPGA | **Lesson 1 done:** FPGA mental model (PS/PL, AXI-Lite vs AXI-Stream, DMA) |
| 2026-10-09 → 10-11 | Radar | **Lesson 2 done:** complex numbers, the FFT as a tuning dial, FMCW chirp → beat frequency, range resolution |
| 2026-10-11 | Radar | **Lesson 3 done:** aliasing (4.5 m target shows at 0.57 m), resolution vs. FFT size, choosing an FFT size. Learned to run Python scripts from PowerShell |
| 2026-10-11 | FPGA | **Lesson 4 done:** two's complement, Q1.15 fixed point, FFT overflow and scaling, packing complex samples, MSB-aligned ADC samples |
| 2026-10-11 | FPGA | Started Harris & Harris ch 1 |
| 2026-10-12 | DCA1000 | Started the Kria-to-Kria link sub-project (helping a labmate replace the DCA1000 capture board). Paused full H&H read-through. |
| 2026-10-12 | DCA1000 | **K1 done:** LVDS (P − N, noise cancelling, 100 Ω termination, the radar's 4 pairs, DDR clock, bit alignment) |
| 2026-10-12 | DCA1000 | **K2 done:** serial protocols (timing vs framing; UART, SPI, I²C, source-synchronous LVDS) |
| 2026-10-12 | DCA1000 | **K3 done:** flip-flops, counters (LED blink math), shift registers (serial receiver = shift register + counter) |
| 2026-10-12 | DCA1000 | **K4 part 1 done:** Verilog module/ports, reg, always/<=, assign. Wrote the loopback design's assign lines. Ready for the lab: 5/6 |
| 2026-10-13 | DCA1000 | **First lab visit:** logged into the KR260 over USB serial and SSH (wired Ethernet only). Board runs stock Ubuntu 22.04, no PYNQ, but has `xmutil`/`fpgautil` to load designs. No lab PC, so installing Vivado 2025.2 ML Standard on my laptop. |
| 2026-10-13 | DCA1000 | **Vivado 2025.2 installed on laptop.** Ready for the lab: 6/6 |
| 2026-10-13 | DCA1000 | **First wiring on the KR260:** checked PMOD4 pin 11 = +3.33 V vs pin 9 with a Fluke 289, lit the LED straight from 3.3 V, then wired the loopback (pin 1 → 330 Ω → LED → pin 9, jumper pin 3 → pin 7). [Photo](dca1000-removal/photos/2026-10-13-first-wiring.jpg) |
| 2026-10-13 | DCA1000 | **First design running on the FPGA (K7 blink, done early):** wrote `loopback.v` by hand, built it in Vivado on my laptop (Zynq block + my module, `pins.xdc`), made `dai_loopback.bit.bin`, copied it to the board with `scp` and loaded it with `xmutil loadapp`. LED blinks through the pin 3 → pin 7 jumper; pulling the jumper out of pin 7 turns it off (pulldown), plugging it back in resumes the blink. |
| 2026-10-14 | DCA1000 | **Board online + PYNQ installed:** David got the KR260 onto a network with internet (verified ping, HTTPS to GitHub, correct clock). Installed Kria-PYNQ (`install.sh -b KR260`, ~30 min, run inside `tmux` so an SSH drop didn't kill it). Jupyter runs on the board at port 9090. Laptop must stay on the lab router's Ethernet to reach the board. |
| 2026-10-14 | FPGA | **Learned the lab's current baseline:** the existing FPGA design does FFT + range + CFAR, and "faster" is measured against a PYNQ Python script on the Kria's ARM cores. Data path today: radar → DCA1000 → Ethernet → PC → Kria. |

## Up next

**DCA1000 removal**
- Finish K4 part 2 (receiver), then K5 (transmitter + receiver in simulation)
- **Next time I meet Person B, ask:** which Vivado version she uses; what her `GPIO_0`–`GPIO_4` connect to; what feeds her DMA's `S_AXIS_S2MM`; can she export her block design (`write_bd_tcl`) or share the project
- Load my loopback design through PYNQ (`Overlay`) to confirm the install end to end

**FPGA and hardware acceleration**
- K7b (AXI GPIO from Python) once PYNQ is on the board
- Lesson 5: the AXI-Stream handshake (feeds K10)

**Radar**
- TI mmWave deck from slide 17

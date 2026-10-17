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
| Kria link lessons (K1–K11 + K7b), [plan](dca1000-removal/PLAN.md), paused 2026-10-17 | `████████░░░░` | 8 / 12: K1, K2, K3, K4, K5, K7, K7b, K10 done |
| Cube bridge (C0–C6), [plan](dca1000-removal/CUBE-BRIDGE.md), current focus | `░░░░░░░` | 0 / 7, C0 formats found, C1 diagnostic started |
| Lab setup (board login, Vivado on laptop, wiring, first bitstream, PYNQ) | `█████` | 5 / 5 ✓ |

Done: [K1 LVDS](lessons/K1-lvds.md) · [K2 serial protocols](lessons/K2-serial-protocols.md) · [K3 flip-flops, counters, shift registers](lessons/K3-flipflops-counters-shift.md) · [K4 Verilog: counter, transmitter, receiver](lessons/K4-verilog-counter.md) · [K5 link in simulation](lessons/K5-serial-link-sim.md) · K7 first design on the board ([lab guide](dca1000-removal/LAB-DAY-1-LAPTOP.md)) · [K7b pins from Python](lessons/K7b-axi-gpio-python.md) · [K10 DMA into memory](lessons/K10-dma-into-memory.md)

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
| 2026-10-14 | DCA1000 | **Loaded my design from Python:** uploaded `dai_loopback.bit` + `dai_loopback.hwh` (copied from the Vivado project's `hw_handoff` folder) to Jupyter and ran `Overlay("dai_loopback.bit")`. LED blinks. One Python line replaces the dtbo/shell.json/xmutil steps. Learned: board shell, laptop PowerShell and the Jupyter notebook each take different commands. |
| 2026-10-14 | DCA1000 | **K4 done:** transmitter (shift right, reload, `frame` on bit 0) and receiver (`rx <= {din, rx[7:1]}`, latch `word` on `frame`). Learned the lab's PMOD loopback receiver uses the same line. Kria link lessons: 5/12 |
| 2026-10-14 | FPGA | **Learned the lab's current baseline:** the existing FPGA design does FFT + range + CFAR, and "faster" is measured against a PYNQ Python script on the Kria's ARM cores. Data path today: radar → DCA1000 → Ethernet → PC → Kria. *(Corrected the same day by Person A's write-up: CFAR isn't in the FPGA yet, and the data goes to the Kria, not a PC.)* |
| 2026-10-15 | DCA1000 | **K5 done:** transmitter + receiver linked in simulation (`word` = b2 at 165 ns). Delaying the data 1 and 2 clocks gave 65 and ca: the bit-alignment problem. Read a real 1 MHz PMOD loopback module: 200 clocks per bit sampled in the middle (survives ~100 clocks of delay), an IDLE/SHIFT/OUTPUT state machine, and the AXI-Stream `tvalid`/`tready` handshake. Kria link lessons: 6/12 |
| 2026-10-15 | DCA1000 | **Ready for K7b:** learned the AXI GPIO (DATA register = pin values, TRI register = direction, 0 = output; starts as all inputs, so `trimask = 0` first), the write mask, and hex-to-binary. Next lab visit: switch an LED on PMOD1 from Python. |
| 2026-10-15 | DCA1000 | **Prepared K7c:** inputs (`trimask = 0x02`), reading one bit with `(value >> n) & 1`, sending a byte from Python through a jumper, and timing a write. Takeaway: if a Python write takes ~8 µs, that's ~4,700× longer than one radar LVDS bit (~1.7 ns), so the bits must be received by FPGA logic; Python only controls it and reads finished data. |
| 2026-10-15 | DCA1000 | **K7b + K7c done at the lab:** switched an LED on PMOD1 from Python (AXI GPIO), read pin 3 through a pin 1 → pin 3 jumper (read 3), sent `10110010` bit by bit and got it back, and measured **13.7 µs per Python write**, about 8,200× slower than one radar LVDS bit. Wrote all the code myself. Kria link lessons: 7/12 |
| 2026-10-15 | DCA1000 | **K10 started:** learned what a DMA is (why reading a register loses numbers, buffers, the DMA's ADDRESS/LENGTH/STATUS registers, `tlast` ends the transfer). Wrote [`counter_stream.v`](dca1000-removal/code/k10/counter_stream.v) (AXI-Stream counter, counts only on a handshake, `tlast` every 1024 words) and its [testbench](dca1000-removal/code/k10/tb.v): 0 to 1023 with no number skipped across a `tready` pause, `tlast` = 1 on 1023. Next: Vivado block design. |
| 2026-10-16 | DCA1000 | **K10 design + Python ready:** built the Vivado block design (Zynq, AXI DMA in simple mode with only the S2MM write channel, counter_stream; DMA registers at 0xA000_0000, DMA writes DDR through HPC0), bitstream timing met (WNS +5.658 ns). Wrote [`k10_dma.py`](dca1000-removal/code/k10/k10_dma.py): load the overlay, allocate a 1024-word buffer, `recvchannel.transfer` + `wait`, check it holds 0 to 1023. Next: run it on the KR260 at the lab. |
| 2026-10-16 | DCA1000 | **K10 done on the KR260:** copied the files over with `scp`, ran [`k10_dma.py`](dca1000-removal/code/k10/k10_dma.py) in Jupyter: printed `[0 1 2 3 4 5 6 7]` and `True`. All 1024 numbers from my PL counter reached DDR memory through the DMA, in order, none missing. [Lesson page](lessons/K10-dma-into-memory.md). |
| 2026-10-17 | DCA1000 | **New focus: the cube bridge.** Person B decodes the raw radar data into a cube; Person A's accelerator runs the FFTs; I bridge the two. Found both formats in the lab code: the radar sends chirp → receiver → sample, the accelerator reads receiver → sample → chirp, so the bridge reorders. Read the lab's carrier-board interface document (frame clock not wired). Paused the Kria link plan. Learned to sync a fork with `upstream` and git LFS. [Plan](dca1000-removal/CUBE-BRIDGE.md). |

## Lab visit 2026-10-15 (K7b + K7c) ✓ done
| Prep | Progress | |
|---|---|---|
| Before going | `████` | 4 / 4 ✓ |

- [x] Lab's LED test design (`led_gpio.bit` + `.hwh`) on my laptop
- [x] Learn what an AXI GPIO is and the Python lines that drive it (DATA and TRI registers, `trimask`, the write mask)
- [x] Know the wiring: LED on PMOD1 instead of PMOD4 (pin 1 → 330 Ω → LED → pin 9)
- [x] Person B questions ready (below)
- [x] K7c (extra): read a pin as input, send a byte from Python through a pin 1 → pin 3 jumper and read it back, time one write

## Up next

**DCA1000 removal**
- **Current:** [cube bridge](dca1000-removal/CUBE-BRIDGE.md), C1 diagnostic quiz then C1 index math. Confirm the input/output formats with Person A and Person B.
- K10 done (2026-10-16). K6, K8 and K9 (true LVDS) wait on the CPSL carrier board; K11 needs K9. K12 (the lab's accelerator) doesn't need LVDS.
- **Next time I meet Person B, ask:** which Vivado version she uses; what her `GPIO_0`–`GPIO_4` connect to; what feeds her DMA's `S_AXIS_S2MM`; can she export her block design (`write_bd_tcl`) or share the project

**FPGA and hardware acceleration**

**Radar**
- TI mmWave deck from slide 17

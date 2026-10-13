# Kria-to-Kria link: lesson plan

**Goal:** get two Kria boards talking over differential (LVDS) wires, and prove it by having one board turn on an LED on the other.

**Why it matters:** this is the first step toward plugging the TI radar straight into a Kria. Today the chain is radar → DCA1000 capture board → Ethernet → PC. The goal is radar → Kria.

**Dai's two goals (restated 2026-10-13):** (1) eliminate the DCA1000, and (2) learn how to **hardware-accelerate** a computation, in a way that carries over to future projects. Every lesson below serves one or both.

---

## The whole system, before anything else

Each lesson below covers one piece of this picture.

**Today:**
1. The TI radar chip (IWR6843) samples the beat signal with its ADC.
2. It sends those samples out over **LVDS**: 2 data lanes, a bit clock, and a frame clock, all as differential pairs. TI's datasheet describes this LVDS port as a debug interface.
3. The **DCA1000** board receives the LVDS. It has its own FPGA (a Lattice ECP5) that turns the lanes back into samples.
4. The DCA1000 streams them to a PC over 1 Gb Ethernet.

**Goal:** steps 3 and 4 are replaced by a Kria. The Kria's FPGA receives the LVDS itself, so the data never leaves the board you're processing it on.

**This sub-project:** before taking on the radar, build the simplest version of step 3 between two boards you fully control. Kria A *transmits* LVDS, and Kria B *receives* it and drives an LED.

---

## The two goals every lesson must serve

1. **Remove the DCA1000.** To replace it, the Kria has to do every job the DCA1000 does today, plus hand the data on:
   - **a. Receive** the radar's LVDS lanes: K1, K2, K5, K6, K8, K9
   - **b. Rebuild samples** from the bits (frame clock, bit alignment): K5, K9
   - **c. Get the samples into memory** where software and Person A's processing can use them: K10
   - **d. Configure and start the radar.** TI's demo firmware takes its settings as text commands over UART, the same settings as `radar_config.py`. K2 introduces UART; K11 uses it.
2. **Learn hardware acceleration, transferable to future projects.** Accelerating means moving a heavy computation (an FFT, backprojection) off the processor and into custom PL logic. It always uses the same loop: **memory → DMA → your compute block → DMA → memory**, with software starting it and reading the result. That loop is built from the system shape below, so goal 2 needs K4–K5 (writing logic), K10 (AXI, DMA) and K12 (the loop itself). Almost every FPGA product has the same shape: **pins → custom logic (PL) → a standard bus (AXI) → memory → a processor running software (PS)**. K1–K9 cover the pins and logic. K10–K11 cover the bus, memory and software. The same shape shows up in quantum control hardware (FPGA logic driving DACs, a CPU running the experiment) and in chip test setups.

| Lesson | DCA1000 job | General FPGA skill |
|---|---|---|
| K1 LVDS | a | high-speed I/O standards |
| K2 serial protocols | a, d | every chip-to-chip interface |
| K3 flip-flops, counters, shift registers | b | the parts every design is built from |
| K4 Verilog | all | writing hardware |
| K5 link in simulation | a, b | verify before hardware |
| K6 pins in Vivado | a | constraints, I/O banks |
| K7 first bitstream | all | the tool flow |
| K8 two boards + ILA | a | bring-up and debugging |
| K9 IDDR/ISERDES | a, b | fast interfaces, clock domains |
| K7b AXI GPIO | c (first step) | software controlling hardware |
| K10 AXI + DMA | c | how logic talks to the processor |
| K11 whole system | c, d | Linux/PYNQ talking to your hardware |
| K12 first accelerator | (Person A's side) | the acceleration loop: memory → DMA → compute → DMA → memory, timed against Python |

---

## One hardware fact that decides a lot

The FPGA's pins are grouped into **banks**, and the bank type decides what a pin can do. These facts come from the AMD docs listed at the bottom:

| Bank type | Voltage | LVDS transmit | LVDS receive | Fast serial blocks (ISERDES/OSERDES) |
|---|---|---|---|---|
| **HP** (high performance) | 1.0–1.8 V | ✅ | ✅ | ✅ |
| **HD** (high density) | 1.2–3.3 V | ❌ | ✅ only with external termination | ❌ |

- **KR260 starter kit:** the PMOD connectors are 3.3 V, which means HD banks, since HP banks max out at 1.8 V. So a PMOD **can't transmit true LVDS**. The KR260 user guide lists its HP banks HPA and HPB for the Ethernet ports, and I haven't found HP pins on any of its user headers.
- **The CPSL custom K26 carrier** (`cpsl-research/kria-k26-CPSL`, branch `lvds_and_can`): it adds two Samtec 60-pin connectors, the same family as the radar ribbon cable. It has LVDS nets named after the radar's pins (4 data, clock, frame clock, valid) and 7 differential pairs each on banks **HPA** and **HPC**. HP banks, so it can do real LVDS both ways.

> **Answer so far (2026-10-12):** two KR260s, connector unknown. With two KR260s, the user headers (PMOD, Raspberry Pi) can't *send* true LVDS. So the plan is:
> 1. Build the link single-ended (`LVCMOS33`) PMOD to PMOD. The logic is identical to the LVDS version (K5), only the pin standard differs.
> 2. Move to true LVDS on the CPSL carrier, which has HP banks wired for it.
>
> **Ask Person B:** "The KR260's PMOD and Pi headers are 3.3 V HD banks, which can't transmit LVDS. Did you mean two KR260s over single-ended pins first, or the CPSL carrier with the Samtec LVDS connectors?"

---

## Person B's block design (screenshot, 2026-10-13)

Person B shared her Vivado block design. It's the PS ↔ PL side of the system above, already built, so K7b, K10 and K11 now use it as the reference instead of starting from a blank design. What's in it (read from the screenshot; what each GPIO is *for* is unknown, so ask her):

| Block | What it does | Lesson |
|---|---|---|
| Zynq, `M_AXI_HPM0_LPD` port | the processor's way to send commands into the PL | K7b |
| `axi_smc` (AXI SmartConnect, 7 outputs) | splits that one port so the processor can reach 7 blocks | K7b |
| `axi_gpio_0` to `axi_gpio_4` → `GPIO_0` to `GPIO_4` | pins the processor sets or reads from software | K7b |
| `axi_dma_0` (`S_AXIS_S2MM` in) → `smartconnect_0` → Zynq `S_AXI_HPC0_FPD` | copies a stream from the PL into the processor's memory | K10 |
| `axi_intc_0` → Zynq `pl_ps_irq0` | lets the PL tell the processor "data is ready" | K10, K11 |
| `clk_wiz_0`, `proc_sys_reset_0/1` | clocks and resets for the blocks above | K10 |
| `xslice_0`: Zynq `emio_ttc0_wave_o` → `fan_en_b` | drives the board fan from a PS timer | K7 (fix) |

**Ask Person B:** what are `GPIO_0`–`GPIO_4` connected to, where does `S_AXIS_S2MM` get its data, and can she export the design (`write_bd_tcl`) or share the project so it can be opened instead of copied by eye?

---

## Lessons

Each lesson is taught in chat in small chunks with a check after each one, then a hands-on task. Labs marked 💻 run on the laptop in a browser. Labs marked 🔧 need the lab PC (Vivado) and the boards.

### K1. What LVDS actually is
- Two wires carry opposite voltages. The receiver only looks at the **difference**, so noise that hits both wires equally cancels out.
- The signal is small (about 350 mV), which makes it fast and low-power. A **100 Ω resistor** across the pair at the receiver (termination) is required.
- The radar's LVDS: 2 data lanes plus a **DDR** bit clock (data on *both* clock edges) and a frame clock that marks where each sample starts. Rates from 150 to 900 Mb/s.
- **Check:** why does the receiver ignore noise? What happens without the 100 Ω termination?

### K2. Serial communication and protocols
- Parallel (many wires, one bit each) vs serial (one wire, bits one after another).
- The core problem of any serial link is that the receiver must know **when** to read each bit and **where** a word starts.
- How the common protocols solve that:
  - **UART:** no clock, both sides agree on a speed
  - **SPI:** a separate clock wire
  - **I²C:** 2 wires, addresses, slow; used to *configure* chips, not to move radar data
  - **Source-synchronous LVDS** (what the radar uses): send a clock pair alongside the data pairs, plus a frame signal for word boundaries
- **Check:** for each protocol, how does the receiver know when to sample?

### K3. The three building blocks of a serial link 💻
- **Flip-flop:** stores 1 bit and updates on a clock edge
- **Counter:** counts clock edges (to know "this is bit 5 of 8")
- **Shift register:** moves bits out one at a time (transmit) or collects them in one at a time (receive)
- **Reading (H&H 2nd ed):** §3.2 Latches and Flip-Flops, §3.3 Synchronous Logic Design, §5.4 Sequential Building Blocks (counters, shift registers)
- **Check:** draw an 8-bit shift register receiving `10110010`, clock by clock.

### K4. Just enough Verilog 💻
- `module`, ports, `wire`/`reg`, `assign`, and `always @(posedge clk)`. That's all the link needs.
- **HDLBits:** Getting Started → Verilog Language: Basics, Vectors, Procedures → Circuits → Sequential Logic: Latches and Flip-Flops, Counters, Shift Registers
- **Reading:** H&H §4.1–4.4 (SystemVerilog column)
- **Do:** write a counter and a shift register yourself.

### K5. Build the whole link in simulation 💻
- Write a **transmitter**: a shift register that sends an 8-bit word, plus a clock output and a frame pulse at the start of each word.
- Write a **receiver**: it shifts bits in on the clock, and on the frame pulse it latches the word and sets `led <= word[0]`.
- Connect them in one testbench on **EDA Playground** and check that the receiver's word matches what was sent.
- Then break it on purpose: shift the clock by half a bit, drop a frame pulse. See what goes wrong, because that's what you'll debug on real hardware.
- **This is the core lesson.** Everything after it is getting this onto real pins.

### K6. Differential pins in Vivado 🔧
- `OBUFDS` (one signal in, a P/N pair out) and `IBUFDS` (a P/N pair in, one signal out) are the primitives that drive and read a pair. Vivado's **Utility Buffer** IP is a block-diagram wrapper around these, which is what Person B mentioned.
- **Constraints (XDC):** `PACKAGE_PIN` for which pin, `IOSTANDARD LVDS` on an HP bank, and `DIFF_TERM_ADV TERM_100` for on-chip 100 Ω termination at the receiver
- Why this only works on HP banks (the table above), and what to do if you're stuck with 3.3 V PMODs: run the K5 link as plain single-ended `LVCMOS33` first. Same logic, just not differential.

### Before K7: get ready for the lab 💻
- **Install Vivado on your laptop.** Free edition (Vivado ML Standard), the **same version as the lab PC (2025.2)**. In the installer, select only the **Zynq UltraScale+** device family. Check first: tens of GB of free disk, ideally 16 GB+ RAM.
- **Test the install:** create an empty project for the K26 and run synthesis on a 1-line design. If that works, the tools are ready.
- **Parts:** jumper wires (have). David confirmed 2026-10-12 the lab has breadboards, LEDs and resistors.
- **Vivado for the first visit:** the lab PC already has it, so the laptop install can come later.
- **Ask the lab for:** the KR260 power supply, USB cable and microSD card, and a multimeter.
- **Pin safety:** PMOD pins are 3.3 V. Never connect one to 5 V, and never wire two outputs together.

### K7. Your first bitstream on one Kria
- **Step-by-step for the first visit:** [LAB-DAY-1.md](LAB-DAY-1.md) 🔧
- **No lab PC / no PYNQ version (what we actually used):** [LAB-DAY-1-LAPTOP.md](LAB-DAY-1-LAPTOP.md)
- The Vivado flow: project → RTL or block design → constraints → synthesize → implement → bitstream → load it on the board
- **Do:** blink an LED on one Kria. This proves your tool flow before two boards are involved.
- **Then wire something:** one jumper wire from one PMOD pin to another on the same board. The FPGA drives the first pin and reads the second back onto an LED. Pull the wire and the LED stops following. This is the first real wiring.
- **Order (changed 2026-10-12, Dai wants lab time early):** do K7 right after K3 plus the counter part of K4, before K5. The blink is just a counter driving an LED.
- Reuses the lab's existing tutorials (`CPSL_Manuals/Kria Board`), = Part C lessons L8–L9 of the main plan.
- **Done 2026-10-13** (laptop + `xmutil` version): hand-written `loopback.v`, blink and jumper test both passed.
- **Fan fix for later designs:** our design leaves `fan_en_b` undriven. Person B's design drives it from the PS timer (`emio_ttc0_wave_o` → slice → `fan_en_b`), like AMD's KR260 designs. Copy that block and its pin constraint from her design next time.

### K7b. The processor flips your LED: AXI GPIO 🔧 (added 2026-10-13, needs PYNQ)
- The smallest possible PS → PL connection, taken from Person B's design: keep the Zynq's `M_AXI_HPM0_LPD` port, add one **AXI GPIO** through a SmartConnect, and wire its output to the PMOD LED pin.
- On the board, Python (PYNQ) writes 1 or 0 to the GPIO and the LED follows. That's the first time software controls your hardware.
- New ideas: an **address** (each AXI block gets one, shown in the Address Editor tab), a **register** (a value at that address), and why Run Block Automation adds the SmartConnect and reset block for you.
- Why now: it's the first piece of K10 and K11, and it's half of Person B's design. Blocked until the board is registered on Duke's network and PYNQ is installed.

### K8. Two boards, one link 🔧
- Load the K5 transmitter onto Kria A and the receiver onto Kria B. Wire P→P and N→N, and **share a ground**.
- Start **slow** (a 1 MHz bit clock), where timing problems can't happen. Toggle the LED from a button or a counter on Kria A.
- Look inside the running FPGA with Vivado's **ILA** (Integrated Logic Analyzer) to see the bits arriving.
- Then raise the speed until it breaks, and learn why. That leads to K9.
- **Done when:** the LED on Kria B follows what Kria A sends.

### K9. Bridge to the radar (Step 2)
- Going faster: **IDDR** (capture on both clock edges, needed for the radar's DDR clock) and **ISERDES** (hardware deserializer). Clock-domain crossing comes in here too; this is main-plan Lesson 5c.
- **Bit alignment:** using the frame clock to find where each sample starts
- Map the radar's real LVDS pins (2 lanes, DDR clock, frame clock) onto your K8 receiver. That's the start of replacing the DCA1000.

### K10. Into memory: AXI-Stream and DMA 💻🔧
- The Kria chip is two halves: **PL** (the FPGA logic you write) and **PS** (4 ARM cores running Linux). They connect through **AXI** buses.
- **AXI-Stream:** a data wire plus two handshake wires, `valid` (sender has data) and `ready` (receiver can take it). A word moves only when both are 1. This is main-plan Lesson 5.
- **DMA:** a block that copies an AXI-Stream into DDR memory without the CPU touching each word.
- **Do:** in simulation, wrap your K9 receiver output as AXI-Stream. On the board, send a counter pattern through AXI DMA into memory and read it in Python (PYNQ), checking that no number is missing.
- **Start from Person B's design:** its `axi_dma_0` → `smartconnect_0` → `S_AXI_HPC0_FPD` path is exactly this. Your counter (later the K9 receiver) drives `S_AXIS_S2MM`. Learn each of her blocks first, then plug yours in, instead of rebuilding the DMA side yourself.
- **Interrupts:** her `axi_intc_0` lets the DMA signal "transfer done" to Linux instead of software checking in a loop.

### K11. The whole system: radar to software, no DCA1000 🔧
- Configure the radar from the Kria over UART (the same settings as `radar_config.py`), start it, receive the LVDS (K9), move the samples into memory (K10), and read one frame in Python.
- Check the result against what you already know from Lesson 3: a target at 1.0 m should show a peak at 1.0 m.
- That frame is what Person A's processing consumes, which closes the loop from radar to result with no DCA1000.

### K12. Your first hardware accelerator 🔧 (added 2026-10-13, goal 2)
- **The loop:** Python puts data in memory → DMA reads it out as a stream (`M_AXIS_MM2S`) → your compute block → DMA writes the result back (`S_AXIS_S2MM`) → Python reads it. Person B's `axi_dma_0` already has both directions, so K12 adds the compute block in the middle.
- **First compute block: an FFT.** It ties to what you know: Lesson 3 (FFT size, aliasing) and Lesson 4 (fixed point, ÷16 scaling). Use AMD's FFT IP first, then compare against the lab's `fpga_fft.py` model (256-point, radix-4).
- **Measure:** time it against NumPy on the Kria's ARM cores, and count FPGA resources (DSPs, BRAM) in Vivado's utilization report. Accelerating is only worth it if the numbers say so, and learning to check that is the transferable part.
- **Then the real target:** main-plan capstones L11–L13: backprojection (the radar imaging step worth accelerating), sizing (does it fit on the chip?) and bit widths. They're paused; K12 is where they rejoin.
- Same loop, different block, in other fields: quantum control (FPGA logic shaping pulses for DACs), chip test, any real-time signal processing.

---

## How the learning works
- **Picture first:** every lesson starts by pointing at where it sits in the system above.
- **Simulate before hardware:** K3–K5 run on the laptop, so by the time you're at the lab, the logic is already proven and only the pins are new.
- **Predict, then run:** before each sim or board test, write down what you expect.
- **Break it on purpose:** each lab includes one deliberate failure, because debugging is most of real FPGA work.
- **Notes:** each lesson gets a notes file in this folder with a "Mistakes I made" section.

## Sources
- AMD UG861, *Differences Between Bank Types* (HP vs HD: LVDS, VCCO, SERDES)
- AMD UG1091, *K26 Carrier Card Design* (HP banks 1.0–1.8 V, HD banks 1.2–3.3 V; carrier supplies VCCO)
- AMD UG1092, *KR260 Starter Kit User Guide* (PMOD is 3.3 V; HP banks used for RGMII Ethernet)
- TI IWR6843 datasheet, LVDS interface (2 data lanes, DDR bit clock, frame clock, 150–900 Mb/s, debug interface)
- Lattice, *DCA1000 Evaluation Module* page (ECP5 FPGA, 2-/4-lane LVDS in, 1 Gb Ethernet out)
- `cpsl-research/kria-k26-CPSL`, branch `lvds_and_can`, `LVDS.kicad_sch`

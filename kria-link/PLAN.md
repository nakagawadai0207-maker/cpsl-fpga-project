# Kria-to-Kria link: lesson plan

**Goal:** get two Kria boards talking over differential (LVDS) wires, and prove it by having one board turn on an LED on the other.

**Why it matters:** this is the first step toward plugging the TI radar straight into a Kria. Today the chain is radar → DCA1000 capture board → Ethernet → PC. The goal is radar → Kria.

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
2. **Understand how FPGAs fit into systems in general.** Almost every FPGA product has the same shape: **pins → custom logic (PL) → a standard bus (AXI) → memory → a processor running software (PS)**. K1–K9 cover the pins and logic. K10–K11 cover the bus, memory and software. The same shape shows up in quantum control hardware (FPGA logic driving DACs, a CPU running the experiment) and in chip test setups.

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
| K10 AXI + DMA | c | how logic talks to the processor |
| K11 whole system | c, d | Linux/PYNQ talking to your hardware |

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

### K7. Your first bitstream on one Kria 🔧
- The Vivado flow: project → RTL or block design → constraints → synthesize → implement → bitstream → load it on the board
- **Do:** blink an LED on one Kria. This proves your tool flow before two boards are involved.
- Reuses the lab's existing tutorials (`CPSL_Manuals/Kria Board`), = Part C lessons L8–L9 of the main plan.

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

### K11. The whole system: radar to software, no DCA1000 🔧
- Configure the radar from the Kria over UART (the same settings as `radar_config.py`), start it, receive the LVDS (K9), move the samples into memory (K10), and read one frame in Python.
- Check the result against what you already know from Lesson 3: a target at 1.0 m should show a peak at 1.0 m.
- That frame is what Person A's processing consumes, which closes the loop from radar to result with no DCA1000.

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

# K10. Into memory: AXI-Stream and DMA

**Where it sits:** the first time numbers made in the FPGA fabric (PL) reached the processor's memory with none lost. Steps 1–2 on 2026-10-15 (Verilog + simulation), steps 3–4 and the board run on 2026-10-16.

**Result on the KR260:** `[0 1 2 3 4 5 6 7]` and `True`: all 1024 numbers from my counter landed in DDR memory, in order, none missing.

## Why a DMA
In K7c, Python read a pin once every 13.7 µs. A PL counter makes a new number every 10 ns, so about 1,370 numbers go by between two Python reads. A DMA copies each number from the PL into memory as it arrives; Python only starts it and reads the result.

## The six things worth knowing
1. **PS vs PL.** PS = the ARM processor running Linux and Python. PL = the programmable logic where my Verilog runs. They are on one chip and talk over AXI.
2. **Control path vs data path.** Control: Python → `M_AXI_HPM0_FPD` → the DMA's `S_AXI_LITE` registers (ADDRESS, LENGTH, STATUS). Data: counter `m_axis` → DMA `S_AXIS_S2MM` → DMA `M_AXI_S2MM` → Zynq `S_AXI_HPC0_FPD` → DDR. Numbers never go through the control path.
3. **Master and slave.** The master starts a transfer, the slave answers. M_ = master port, S_ = slave port. The PS is master on the control path; the DMA is master when it writes memory.
4. **The AXI-Stream handshake.** A word moves only on a clock where `tvalid` (sender has data) and `tready` (receiver can take it) are both 1. `tlast` = 1 marks the last word of a packet and ends the DMA transfer.
5. **DMA in simple mode.** Python writes ADDRESS (where the buffer starts), then LENGTH (writing it starts the DMA), then waits for STATUS = done, then reads the buffer. LENGTH is the maximum; `tlast` ends it.
6. **The address map.** Every block the PS can reach has an address (here, the DMA's registers at `0xA000_0000`). The `.hwh` file carries this map to PYNQ, which is why the `.bit` and `.hwh` names must match.

## Who does what, step by step

| # | What happens | Who | Path |
|---|---|---|---|
| | **Setup** | | |
| 1 | `Overlay(...)` loads the design into the PL and reads the `.hwh` | Python (PS) | setup |
| 2 | `dma = ol.axi_dma_0` gets a handle to the DMA | Python (PS) | none |
| 3 | `allocate(...)` reserves 1024 slots in DDR memory | Python (PS) | none |
| | **Start: `transfer(buf)`** | | |
| 4 | Write the buffer start address to DMA register `0xA000_0048` | Python (PS) | control |
| 5 | Write the length (4096 bytes) to DMA register `0xA000_0058`; this starts the DMA | Python (PS) | control |
| | **Filling the buffer (no Python)** | | |
| 6 | Counter puts a number on `m_axis_tdata`, `tvalid` = 1 | PL (my Verilog) | data |
| 7 | On a clock where `tvalid` and `tready` are both 1, the word moves into the DMA | PL (counter + DMA) | data |
| 8 | DMA writes the word into DDR at the next address (+4) through HPC0 | PL (AXI DMA block) | data |
| 9 | Counter adds 1, only after a handshake | PL (my Verilog) | inside counter |
| 10 | Steps 6 to 9 repeat; on word 1023 `tlast` = 1 | PL | data |
| 11 | DMA sees `tlast`, finishes, sets its status register to done | PL (AXI DMA block) | inside DMA |
| | **Finish: `wait()` and check** | | |
| 12 | Read status register `0xA000_0034` until it says done | Python (PS) | control |
| 13 | `print(buf[0:8])` and `array_equal` read the buffer from DDR | Python (PS) | memory read |

For the radar, only steps 6 and 9 change: the LVDS receiver (PL) replaces the counter. Register offsets checked against PYNQ's `pynq/lib/dma.py` (S2MM block at +0x30: status +0x04, address +0x18, length +0x28).

## What I built
- [`counter_stream.v`](../dca1000-removal/code/k10/counter_stream.v): AXI-Stream counter. Counts only on a handshake, so a `tready` pause never skips a number; `tlast` every 1024 words. [Testbench](../dca1000-removal/code/k10/tb.v) passed in Icarus.
- Vivado block design `k10_bd`: Zynq (KR260 preset), AXI DMA 7.1 (simple mode, S2MM only, 64-bit addresses, 14-bit length), my counter, smartconnects and reset block. Timing met: WNS +5.658 ns at 100 MHz.
- [`k10_dma.py`](../dca1000-removal/code/k10/k10_dma.py) in PYNQ: `Overlay`, `allocate(shape=(1024,), dtype=np.uint32)`, `dma.recvchannel.transfer(buf)`, `dma.recvchannel.wait()`, compare with `np.arange(1024)`. `recvchannel` = the S2MM (stream to memory) side; `sendchannel` would be MM2S.

## Why it matters for the DCA1000
This is the path radar samples will take. Later, the receiver that rebuilds samples from the radar's LVDS bits replaces the counter at the front, and everything after it stays the same.

## Mistakes I made
- Verilog: width after the name, `10b'` instead of `10'b`, nine 1s instead of ten, `$time;` on its own line.
- Said `tvalid` comes from the DMA and `tready` from the Zynq (`tvalid` is the counter's, `tready` the DMA's); first plugged the counter into `M_AXI_S2MM` (it's `S_AXIS_S2MM`).
- Added AXI Central DMA (CDMA) instead of AXI DMA.
- Python: `from pynq import np`, `NumPy` with capitals, `wait` without `()`, `np.arrange`, Verilog-style `"%0b"` in `print`.
- Ran `scp` on the board instead of the laptop; Jupyter didn't find the files in `~/dai` until I gave `Overlay` the full path.

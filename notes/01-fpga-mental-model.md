# Lesson 1: the FPGA mental model

## What an FPGA is
A chip full of small, rewirable building blocks:
- **LUTs** (look-up tables) do any small logic function.
- **Flip-flops** store one bit each, updated on a clock edge.
- **BRAM** is on-chip memory.
- **DSP slices** are hard multiply-add units, which is where the signal-processing math goes.
- **Routing** is the programmable wiring between all of these.

The **bitstream** is the file that sets up all that wiring. It's *volatile*: it disappears at power-off and has to be reloaded.

The K26 module on the KR260 has 1,248 DSP slices, about 26.6 Mb of on-chip memory, and 4 GB of DDR4.

## PS vs PL (Zynq)
- **PS (processing system):** ARM CPU cores running Linux and Python. Flexible, but each core does one thing at a time.
- **PL (programmable logic):** the FPGA fabric. It does lots of things at once, every clock cycle.
- Speed-up pattern: the PS stays in charge, and the heavy, regular math moves to the PL.

## Moving data between them
- **AXI-Lite:** small control registers ("start", "size = 1024", "done?"). Slow and low bandwidth.
- **AXI-Stream:** a firehose of samples using a valid/ready handshake. This is where radar data flows.
- **DMA:** a copy engine that moves big buffers between DDR memory and the PL. The CPU stays free for other work while the DMA copies.
- **PYNQ:** Python on the board. It loads a `.bit` (bitstream) plus a `.hwh` (hardware description) and lets you drive the PL from Python.

## Mistakes I made
- Swapped AXI-Lite and AXI-Stream at first. Lite = control, Stream = data.

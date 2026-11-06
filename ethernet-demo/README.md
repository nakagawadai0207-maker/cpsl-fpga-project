# Ethernet demo

**Goal (from 2026-11-06):** a working demo where the radar's raw data reaches the Kria as Ethernet packets (TI DCA1000 capture card → router → Kria), and the lab's range–Doppler FFT accelerator in the Kria's fabric turns each frame into a map.

**Why the pivot:** the custom PCB that would have carried the radar's LVDS lanes straight into the Kria isn't working, and probably won't be soon. So the direct-LVDS work in [DCA1000 removal](../dca1000-removal/) is on hold, and the demo keeps the DCA1000 and its Ethernet link.

**My part:**
1. Understand every step from "what's inside one Ethernet packet" to "the accelerator gets correctly ordered data".
2. Then find out whether that path can be made faster by cutting out middle steps (in software or in HDL), and whether it's worth doing.

## What I've learned for this
- **Packets → frame:** each DCA1000 packet carries a sequence number (spots lost packets) and a byte count (where its bytes go). Frame = count // frame size, position = count % frame size, so a lost packet only leaves a hole in its own frame. ([E1–E2](../lessons/E1-E2-packets-to-frame.md))
- **Bytes → numbers:** two bytes, low first, make one signed 16-bit number; the numbers come in groups of four, `[Q_a, Q_b, I_a, I_b]`, holding two complex samples. ([E3](../lessons/E3-bytes-to-numbers.md))
- **Numbers → cube:** samples arrive chirp by chirp, RX by RX (252 per chirp); `reshape(210, 4, 63)` reads that line as the (chirp, RX, sample) cube without moving data. ([E4](../lessons/E4-numbers-to-cube.md))

## Plan
- [**PLAN.md**](PLAN.md): lessons E1–E6 (the path) and O1–O5 (optimizing it)

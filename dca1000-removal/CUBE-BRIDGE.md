# Cube bridge: from the decoded radar data to the FFT accelerator

**Started 2026-10-17. Current focus.** The Kria-to-Kria link plan ([PLAN.md](PLAN.md)) is paused while I do this.

## The assignment

- **Person B** receives the raw radar data, which comes with headers. She finds the headers, splits the stream into chirps and samples, and assembles the **radar cube** (4 receivers × 63 samples × 210 chirps, 16-bit I and Q).
- **Person A's** FPGA accelerator takes a cube and runs the range and Doppler FFTs.
- **Me:** the bridge between them.

**In one sentence:** I receive Person B's decoded radar frame (the raw I/Q samples for every chirp and receiver, still in the order the radar sent them), and I output the same frame reordered into the cube layout Person A's accelerator reads (receiver, sample, chirp), placed directly in its input buffer.

## What the bridge has to get right

1. **Shape:** 4 × 63 × 210.
2. **Order in memory:** the radar sends chirp first, then receiver, then sample. The accelerator reads receiver, sample, chirp. So the data has to be reordered.
3. **Number format:** the radar packs I and Q in its own pattern, and the accelerator wants (real, imag) pairs of int16.
4. **Handoff:** the frame should land in the accelerator's input buffer without the CPU copying it.

A software version of the decode-and-reorder already exists in the lab's code. So the real new contribution is doing the reorder **inside the FPGA**, for when the radar's LVDS goes straight into the fabric with no DCA1000. Sending the data up to Python just to reorder it would bring back the slow CPU step that removing the DCA1000 is meant to eliminate.

## Steps

| Step | What | Status |
|---|---|---|
| C0 | Agree on the input and output formats with Person A and Person B | formats found in the code; waiting on their confirmation |
| C1 | Index math: where each (receiver, sample, chirp) value sits in one flat buffer | diagnostic quiz in progress |
| C2 | Test pattern: fake data where every number encodes its own position, so any mix-up shows | |
| C3 | Fake target at a known distance and speed: the FFT must put it in the right bin | |
| C4 | Software bridge on the KR260: feed a frame to the accelerator and compare with NumPy (minimum demo) | |
| C5 | No-copy handoff: the data lands directly in the accelerator's buffer (uses [K10](../lessons/K10-dma-into-memory.md)) | |
| C6 | Do the reorder in FPGA logic, for the LVDS path | |

## End product to show David

A notebook on the KR260 that takes a decoded frame, sends it through the bridge into the accelerator, and shows the range–Doppler map next to NumPy's. It prints a layout test PASS, the fake target landing in the right bin, and how long the handoff takes. Plus a one-page interface agreement signed off by both labmates.

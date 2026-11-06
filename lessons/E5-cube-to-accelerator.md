# E5: From the cube into the FFT accelerator

Part of the [Ethernet demo](../ethernet-demo/) ([plan](../ethernet-demo/PLAN.md)). Done 2026-11-06. Recap of what I ran on the Kria in [cube bridge](../dca1000-removal/CUBE-BRIDGE.md) C4.

1. **Reorder** (my bridge): `np.ascontiguousarray(np.transpose(cube_b, (1, 2, 0)))` turns (210, 4, 63) chirp-RX-sample into (4, 63, 210) RX-sample-chirp, the order the accelerator reads.
2. **Pack** into the DMA buffer `ibuf`: each complex sample becomes two 16-bit integers (I, Q). A **buffer** is a block of memory set aside for data in transit; `ibuf` is reserved in DDR with PYNQ's `allocate` so it is one unbroken block the DMA can read.
3. **Flush, DMA, FFTs:** flush `ibuf` (the DMA reads DDR, not the CPU's cache) → arm the receive channel → send `ibuf` into the fabric → range FFT, Doppler FFT, power, fftshift in the fabric → wait → invalidate `obuf` → read the range–Doppler map.

## The middleman I noticed
The samples arrive as 16-bit integers, get converted to floats/complex numbers by the decoder, then get packed back into 16-bit integers for the fabric. The decoder does three jobs: unscramble the I/Q groups (needed), reorder the cube (needed), and convert to floats (only needed for FFTs done in software). For the hardware path, the first two could run directly on the integers. This becomes lesson O3.

## Mistakes I made
- Gave the order (RX, sample, chirp) when asked for the shape; the shape is the sizes, (4, 63, 210).

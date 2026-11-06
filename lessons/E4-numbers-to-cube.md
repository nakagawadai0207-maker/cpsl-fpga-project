# E4: From a line of samples to the radar cube

Part of the [Ethernet demo](../ethernet-demo/) ([plan](../ethernet-demo/PLAN.md)). Done 2026-11-06.

- After E3 there is one long line of complex samples. The DCA1000 sends them chirp by chirp, and inside each chirp RX by RX: samples 0–62 are chirp 0 RX 0, 63–125 chirp 0 RX 1, 126–188 chirp 0 RX 2, 189–251 chirp 0 RX 3.
- One chirp is 4 RX × 63 samples = 252 samples, so sample 252 is `[1, 0, 0]`: the first sample of chirp 1.
- `line.reshape(210, 4, 63)` turns the line into the (chirp, RX, sample) cube. reshape moves no data; it only changes how the line is read. This is the same cube order as in the [cube bridge](../dca1000-removal/CUBE-BRIDGE.md) (C0).

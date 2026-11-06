# E6: The whole path, and who does what

Part of the [Ethernet demo](../ethernet-demo/) ([plan](../ethernet-demo/PLAN.md)). Done 2026-11-06.

Order, network to map: **receiver** (packets → frame) → **decode** (I/Q unscramble, complex numbers, and the reorder to RX-sample-chirp) → **pack into `ibuf`** → **DMA + FFTs**.

| Step | Who | Software or hardware |
|---|---|---|
| Packets arrive | network port + Linux | OS (kernel, also on the ARM) |
| Receiver (→ frame) | ARM, Python | software |
| Decode (complex + reorder) | ARM, Python | software |
| Pack into `ibuf` | ARM, Python | software |
| Flush | ARM | software |
| DMA + FFTs | DMA + fabric | hardware |
| Invalidate + read map | ARM, Python | software |

Four Python/ARM steps (receiver, decode, pack, flush) happen before the data reaches the fabric, plus the kernel's own network handling. Those are the candidates for optimizing in part 2.

Correction I got: in the lab's real decoder, the reorder happens inside decode; in my C4 test it was a separate line only because I built the cube myself.

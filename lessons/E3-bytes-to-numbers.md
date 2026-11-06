# E3: From raw bytes to I/Q samples

Part of the [Ethernet demo](../ethernet-demo/) ([plan](../ethernet-demo/PLAN.md)). Done 2026-11-06.

- **Two bytes → one 16-bit number, low byte first (little-endian):** `n = high × 256 + low`. Bytes [10][2] → 2 × 256 + 10 = 522.
- **Signed (two's complement):** if `n ≥ 32,768`, the number is negative: `n − 65,536`. Bytes [255][255] → 65,535 − 65,536 = −1 (all bits 1 is −1).
- **I and Q:** each sample is complex, I + jQ. For our radar (IWR6843 through the DCA1000), the numbers come in groups of four holding two samples, Q's first: `[Q_a, Q_b, I_a, I_b]`. Group [7, −3, 20, 5] → sample a = 20 + 7j, sample b = 5 − 3j.

## Mistakes I made
- Swapped high and low byte: wrote 10 × 256 + 2 for bytes [10][2]. The second byte is the high one.
- Subtracted the wrong way for a negative number (65,536 − n instead of n − 65,536).

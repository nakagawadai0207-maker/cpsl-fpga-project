# E1–E2: From Ethernet packets to one radar frame

Part of the [Ethernet demo](../ethernet-demo/) ([plan](../ethernet-demo/PLAN.md)). Done 2026-11-06.

## E1: what is in one packet
The DCA1000 capture card doesn't send a radar frame in one piece. It cuts the stream of samples into UDP packets. Each packet is:

```
| header (10 bytes)                 | payload (up to ~1,462 bytes) |
| sequence number | byte count      | raw radar samples            |
```

- **Sequence number:** counts packets 1, 2, 3, … A jump (7, 8, 10) means a packet was lost (9).
- **Byte count:** how many sample bytes were sent *before* this packet. It is exactly where this packet's bytes belong in the stream.
- One frame in our setup is 211,680 bytes, so it takes 211,680 / 1,462 ≈ 144.8 → **145 packets** (the last one is partly full).

## E2: packets → one frame
The byte count never resets, so frames sit back to back in one long stream.

- **Which frame:** `byte_count // frame_bytes` (integer division). Byte count 500,000 → 500,000 // 211,680 = **frame 2**.
- **Where inside it:** `byte_count % frame_bytes`. 500,000 % 211,680 = **76,640**.
- **A lost packet** leaves a hole of zeros in that one frame only, because every other packet is still placed at its own position. If the receiver instead glued packets together in arrival order, one lost packet would shift every byte after it and ruin every later frame (the same problem the frame clock solves on LVDS wires).
- **Hand-off:** a frame is handed to processing when all 211,680 bytes have arrived, or, if a packet was lost, as soon as data for the next frame shows up (marked incomplete).

## Mistakes I made
- Said a packet with byte count 4,386 goes at position 0. The byte count *is* the position: 4,386.

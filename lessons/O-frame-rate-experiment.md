# Frame-rate experiment: how fast can the Ethernet path go?

Part of the [Ethernet demo](../ethernet-demo/). Done 2026-11-08 on the lab's Kria, using its radar dashboard, with the owner's OK. Exact lab numbers are kept in the lab's private notes; this page records what I learned.

## What I did
1. I recorded radar fps, processed fps, latency and dropped packets at 20 fps, then stepped the frame rate up to about 91 fps.
2. Hand test: I moved my hand fast toward the radar, holding something metal, once at 20 fps and once at 50 fps.
3. I set the frame rate back to 20 fps and checked the system was healthy.

## What I found
- The Kria can **process** only so many frames per second. Above that limit it skips frames, but the display stays live.
- At higher rates, **packet capture** in Python falls behind. Unread packets pile up in Linux's receive buffer, which is a block of memory where packets wait. When the buffer is full:
  - every new packet waits behind the whole buffer, which gave a delay of several seconds (delay = buffer size / read rate)
  - packets that don't fit are thrown away whole, and each one leaves a hole of zeros in its frame, which shows as flashing
- A bigger buffer doesn't fix this. It only makes the delay longer. Big buffers help only when the reader is faster on average and just has short busy moments.
- **Faster chirps fix fast-motion speed readings.** At 20 fps, a fast hand move wrapped around the speed axis and showed up on the wrong side. At 50 fps the same move read correctly. *Correction:* what fixed it was the shorter idle time between chirps that the faster setting uses, not the frame rate itself. Max speed = wavelength ÷ (4 × time between chirps from the same transmitter). A 33 fps setting with short idle times reaches the same limit as 50 fps.
- The best usable rate today is about 2.5× the default, with no drops and no delay. To go higher, capture needs its own process (Python threads can't run in parallel because of the GIL).

## Mistakes I made
- I thought the delay was the time for the buffer to *fill*. It's actually how long each packet waits once the buffer is full.
- I thought the *old* data gets thrown away. It's the *new* packets arriving at a full buffer that get dropped.
- I'd forgotten that a lost packet leaves zeros (from E2).

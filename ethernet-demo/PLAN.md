# Ethernet demo: lesson plan

Taught in small steps with a check after each one. Each lesson gets notes in [lessons/](../lessons/).

## Part 1: the path, packet to accelerator

| # | Lesson | Question it answers |
|---|---|---|
| E1 | One packet | What is inside one DCA1000 UDP packet? (header: sequence number + byte count; payload: raw samples) |
| E2 | Packets → one frame | How do hundreds of packets get put back together into one radar frame, and what happens when one is lost? |
| E3 | Bytes → numbers | How do raw bytes become 16-bit I and Q values? (little-endian, the order the I/Q values come in) |
| E4 | Numbers → cube | How do those values become the (chirp, RX, sample) cube? Links to [cube bridge](../dca1000-removal/CUBE-BRIDGE.md) C0–C2 |
| E5 | Cube → accelerator | Reorder to (RX, sample, chirp), pack into the DMA buffer, flush, DMA into the fabric. Links to cube bridge C4 |
| E6 | Whole-path map | Who does what at each step: network card, Linux, Python, DMA, fabric |

## Part 2: making it faster, and whether it's worth it

| # | Lesson | Question it answers |
|---|---|---|
| O1 | Measure | How long does each step actually take on the Kria? (same timing method as C4) |
| O2 | Is it worth it? | Frame budget vs. measured time; what limits frames per second; the network's own transfer time |
| O3 | Software shortcut | Can Python skip extra copies and conversions without any HDL? |
| O4 | Reorder in the fabric | An HDL block that unscrambles and reorders the samples so the ARM doesn't have to |
| O5 | Ethernet into the fabric | The KR260 has two Ethernet ports wired to the fabric; what receiving packets in logic would take, and whether it's in scope |

**Decision point after O2:** only go on to O3–O5 if the measurements show the path is worth speeding up.

## Part 3: multi-core capture (chosen 2026-11-08)

The [frame-rate experiment](../lessons/O-frame-rate-experiment.md) showed that at high frame rates, Python's packet receiver falls behind. It runs as a *thread* next to the processing thread, and Python's GIL lets only one of them run at a time. The fix is to move the receiver into its own *process*, so it runs on a separate ARM core. I chose this over Ethernet-in-fabric (O5) because it's smaller, low-risk, and fixes the measured bottleneck.

**Hypothesis:** the separate process removes the multi-second delay and the dropped packets, and also raises processed frames per second, because processing stops waiting for the receiver. Cutting decode time afterward should reach the radar's maximum frame rate. The speed limit (max m/s) is set by the radar's chirp timing, so this won't change it.

| # | Lesson | Hands-on | Data |
|---|---|---|---|
| M1 | Process vs thread, and the GIL | same CPU-busy job in 2 threads vs 2 processes, timed on the Kria | speedup |
| M2 | How the current receiver works | read the receiver: packets, sequence numbers, frame assembly, newest-frame queue | (understanding) |
| M3 | Is capture alone fast enough? | capture-only script at high frame rates | packets/s, drops |
| M4 | Passing a frame between processes | `multiprocessing.shared_memory` demo | ms per frame handoff |
| M5 | Capture in its own process | `multiprocessing.Process` + shared-memory frame slots | frames arrive in the main process |
| M6 | Connect processing | newest frame → decode → FPGA | before/after table across frame rates |
| M7 | (Stretch) parallel decode | decode in another process while the FPGA works | processed fps |
| M8 | Deliverable | before/after table, 2 plots, one-page write-up for my mentor and the lab member who owns the code, code they can merge | report + code |

Rules: I work on copies in my own folder; the lab's running service and code aren't modified. Live tests need the service paused, with the owner's OK each time.

## Status
- 2026-11-06: plan written. Next: E1.
- 2026-11-08: Part 1, O1–O2 and the frame-rate experiment done. Part 3 (multi-core) planned. Next: M1.

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

## Status
- 2026-11-06: plan written. Next: E1.

# K2. Serial communication and protocols

**Where it sits:** K1 was how one bit travels on a pair of wires. K2 is how a receiver turns a stream of bits back into numbers, and which protocol each part of the radar system uses.

## 1. Parallel vs serial
- **Parallel:** one wire per bit, all at once. 8 bits = 8 wires, 1 clock tick.
- **Serial:** bits one after another on one wire or pair. 8 bits = 8 ticks.
- Serial wins on **pin count** (the radar sends 16-bit samples on 2 pairs) and **speed** (no **skew** between wires of slightly different lengths).
- Every serial receiver has two jobs:
  - **Timing:** *when* to read each bit (read near the middle of the bit)
  - **Framing:** *where* each word starts
- Example: 16 bits at 600 Mb/s = 16 ÷ (600 × 10⁶) = 26.7 ns on one lane, 13.3 ns split across two lanes.

## 2. UART (no clock wire)
- **Timing:** both sides agree on a **baud rate** in advance. At 115,200 bits/s each bit lasts 8.68 µs.
- **Framing:** the line idles at 1. A byte is a **start bit** (0), then 8 data bits (lowest first), then a **stop bit** (1).
- The receiver sees the drop to 0, waits 1.5 bit times to land in the middle of data bit 0, then reads every bit time.
- 10 bits on the wire per byte, so 115,200 bits/s = **11,520 bytes/s**.
- Clock mismatch drifts the reading point, so UART stays slow and short. **The radar's settings go over UART** as text commands.

## 3. SPI (clock wire)
- 4 wires: **SCLK** (clock), **MOSI** (controller → chip), **MISO** (chip → controller), **CS** (chip select, low = active).
- **Timing:** the clock wire, so no agreed speed and no drift. Typically 10–50 MHz.
- **Framing:** CS going low; then count 8 clock edges per byte. No start/stop bits.
- 2 bytes at 10 MHz = 16 ÷ (10 × 10⁶) = 1.6 µs. If SCLK breaks, **timing** fails.

## 4. I²C (two shared wires)
- **SCL** (clock) and **SDA** (data, both directions), shared by every chip on the bus.
- Each chip has a **7-bit address**; only the matching chip responds.
- **Framing:** start = SDA drops while SCL is high; stop = SDA rises while SCL is high.
- **ACK:** receiver pulls SDA low after each byte. No ACK = no chip answered (check first when debugging).
- 100 or 400 kHz. One-byte write ≈ 20 bit times (start + 7 address + R/W + ACK + 8 data + ACK + stop): 200 µs at 100 kHz, 50 µs at 400 kHz.
- Used for configuring helper chips, never for radar data.

## 5. Source-synchronous LVDS (the radar)
- The sender transmits its own clock beside the data. Clock and data share the same delay, so edges stay lined up at the receiver: up to 900 Mb/s per lane.
- **Frame clock** marks the first bit of every sample (SPI's CS only marks the start of a transaction).
- DDR + LVDS pairs.
- **LVDS itself is not a protocol.** It's an electrical standard (a bit = P − N = ±0.35 V). The protocol is source-synchronous (bit clock + frame clock + data lanes), and it runs on LVDS pairs.
- A **protocol** = the rules both sides follow: which wires, how timing works, how framing works. Real systems use several at once: UART for radar settings, the LVDS link for samples, I²C for helper chips on the board.

| | Wires | Timing | Framing | Speed | Used for |
|---|---|---|---|---|---|
| UART | 1 per direction | agreed baud rate | start bit | ~115 kb/s | radar settings (text commands) |
| SPI | 4 | clock wire | CS | 10–50 Mb/s | chip ↔ processor |
| I²C | 2, shared | clock wire | start/stop + address | 100–400 kb/s | configuring helper chips |
| Radar LVDS | 4 pairs | bit clock, DDR | frame clock | 150–900 Mb/s per lane | streaming ADC samples |

## Mistakes I made
- UART bytes/s: divided by 8 instead of 10. Count the start and stop bits.
- Radar settings: picked SPI by reasoning about speed. The real answer is UART, because that's what the radar firmware accepts. Check what the chip actually supports first.

# K1. What LVDS actually is

**Where it sits:** the radar chip sends its ADC samples out over LVDS. Today the DCA1000 receives them. The goal is for the Kria to receive them.

## 1. One bit on two wires
- A normal (single-ended) signal is one wire measured against ground. On a 3.3 V pin, about 3.3 V reads as 1 and about 0 V reads as 0.
- LVDS uses two wires per signal, **P** and **N**, which the driver always pushes in opposite directions.
- The receiver measures only **P − N**:
  - above +0.1 V → 1
  - below −0.1 V → 0
  - between −0.1 V and +0.1 V → not guaranteed either way
- Typical values: both wires sit around 1.2 V.
  - Sending a 1: P = 1.375 V, N = 1.025 V → **+0.35 V** → 1
  - Sending a 0: the values swap → −0.35 V → 0
- A small swing switches faster and uses less power, which is why the radar uses LVDS for data up to 900 Mb/s.

## 2. Why noise cancels
- P and N are routed side by side, so noise hits both by almost the same amount.
- Example: +0.5 V on both wires while sending a 1 gives P = 1.875 V, N = 1.525 V. P − N is still +0.35 V.
- Noise on **one** wire doesn't cancel. Example: +0.3 V on P only while sending a 0 gives P − N = −0.05 V, which is in the gap.
- Limit: LVDS receivers work only while both wires stay roughly between 0 V and 2.4 V.

## 3. The 100 Ω termination resistor
- The driver pushes a fixed **current** (about 3.5 mA) out on P, through a 100 Ω resistor at the receiver, and back on N.
- V = I × R = 0.0035 A × 100 Ω = **0.35 V**. That's where the swing comes from.
- With a wrong resistor value the swing changes: 3.0 mA × 50 Ω = 0.15 V, so only 0.05 V of noise reaches the gap.
- Without the resistor, the swing is uncontrolled, and at high speed each edge reflects off the open end of the wire and smears into the next bits.
- Kria: **HP** banks have the resistor built in (`DIFF_TERM` setting in Vivado). **HD** banks (the KR260's PMOD pins) need a physical resistor.

## 4. The radar's LVDS port
- 4 pairs: **2 data lanes**, a **bit clock** (when to read each bit), and a **frame clock** (where each sample starts).
- **DDR:** a bit is read on both the rising and falling clock edge, so the clock runs at **half** the bit rate.
  - 400 Mb/s → 200 MHz clock
  - 900 Mb/s (radar max) → 450 MHz clock
- Each sample is 16 bits in one unbroken stream. Starting one bit late doubles the value (3 → 6, 5 → 10), and nothing flags the error. Fixing this is **bit alignment** (K9).

## Mistakes I made
- P − N = 1.325 − 1.375: I said 0, but it's −0.05 V. The conclusion (in the gap, not guaranteed) was still right.
- DDR clock: I multiplied by 2 (400 → 800). The clock is the bit rate **divided** by 2, because each cycle carries 2 bits.

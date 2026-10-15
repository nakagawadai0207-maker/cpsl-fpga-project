# K7b + K7c. Controlling PMOD pins from Python (AXI GPIO)

**Where it sits:** the first time Python on the Kria's ARM cores (PS) talked to a block in the FPGA fabric (PL). Done at the lab on 2026-10-15, with PYNQ in Jupyter and the lab's LED test design (three AXI GPIO blocks, one per PMOD).

## What an AXI GPIO is
- A small block in the PL with registers that the PS can read and write over AXI-Lite. Each bit of a register is one pin.
- **DATA** register: the pin values. Writing sets the output pins; reading gives the value on every pin.
- **TRI** register: the direction of each pin. **0 = output, 1 = input.** The design starts with every pin as an input, so a pin must be made an output before writing does anything.
- PMOD bit to pin (8 bits): bits 0–3 are pins 1, 3, 5, 7; bits 4–7 are pins 2, 4, 6, 8. Pin 9 = GND, pin 11 = 3.3 V.

## The Python (PYNQ)
- `Overlay("….bit")` loads the design into the PL; `ol.axi_gpio_0.channel1` is PMOD1's 8 pins.
- `gpio.trimask = …` writes the TRI register. (PYNQ's `setdirection()` does **not** write TRI.)
- `gpio.write(value, mask)` changes only the bits that are 1 in `mask`: new = (old AND NOT mask) OR (value AND mask).
- `gpio.read()` returns all 8 pins as one number. One bit: `(value >> n) & 1`.

## What I did at the lab
1. LED on PMOD1 (pin 1 → 330 Ω → LED → pin 9), `trimask = 0`, wrote bit 0 high and low: the LED switched.
2. `trimask = 0b00000010` (pin 3 = input) **before** plugging in a pin 1 → pin 3 jumper, so two outputs never fight. Wrote pin 1 high, read **3** (bits 0 and 1 set).
3. Sent `10110010` one bit at a time (bit 0 first) on pin 1, read each back on pin 3 and rebuilt it with `received |= rx << i`: got `0b10110010`.
4. Timed 10,000 writes with `time.perf_counter()`: **13.7 µs per write.**

## Why it matters for the DCA1000
One radar LVDS bit lasts ~1.7 ns (600 Mb/s per lane). 13.7 µs ÷ 1.7 ns ≈ **8,200×** too slow. Python can't handle radar bits one at a time; FPGA logic has to receive them, and Python only configures it and reads the finished data from memory (K10, DMA).

## Mistakes I made
- Typed `ol.axi.gpio_0` instead of `ol.axi_gpio_0` (AttributeError).
- Edited the setup cell but didn't re-run it, so the board was still on the old TRI setting.
- First read gave 1 instead of 3: the jumper wasn't on pin 3 properly.
- Used `&&` (not Python) instead of `&`.
- `print(t1 - t0/n * 1000000)` gave a negative number: `/` and `*` run before `-`, so the subtraction needed parentheses.
- Earlier, while preparing: read hex `0x04` as "bits 0–3", mapped bit 2 to pin 3 (it's pin 5), and mixed up the write mask with `trimask`.

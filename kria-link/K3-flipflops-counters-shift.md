# K3. Flip-flops, counters, shift registers

**Where it sits:** the K5 transmitter and receiver are built entirely from these three parts. The blink in the first lab is a counter.

## 1. D flip-flop
- Stores 1 bit. Input **D**, **clock**, output **Q**.
- **Rule:** at each rising clock edge, Q copies D. Between edges, Q holds, whatever D does.
- A change in D that comes and goes between two edges is never stored.
- Every flip-flop updates on the same edge, so the whole circuit changes in step once per clock. The K26 chip has roughly 234,000 of them.
- Example (edges every 10 ns): D = 0 at 0 ns, 1 at 6 ns, 0 at 22 ns → Q = 0 at 8 ns, 1 at 15 ns, still 1 at 25 ns (next edge is 30 ns).

## 2. Counter
- A few flip-flops holding a binary number, plus an adder. Each rising edge stores value + 1.
- N flip-flops count 0 to 2ᴺ − 1, then wrap to 0. Counting positions 0–15 needs **4** flip-flops (2⁴ = 16 values; 15 = `1111`).
- Bit k flips every 2ᵏ edges.
- **Blinking an LED:** 100 MHz clock (10 ns per edge), LED on a high bit.
  - bit 26: 2²⁶ × 10 ns ≈ 0.67 s on, 0.67 s off
  - bit 24: 2²⁴ ÷ 10⁸ ≈ 0.17 s on, 0.17 s off
- In a serial receiver, a counter tracks bit position; the wrap to 0 means "word complete."

## 3. Shift register
- Flip-flops in a chain: each Q wired to the next D.
- Each rising edge, every bit moves one place. The new bit enters on the right; the leftmost falls off.
- **Receive (serial → parallel):** after N edges, N bits sit side by side and can be read at once.
- **Transmit (parallel → serial):** load a word at once, shift it out 1 bit per edge.
- Example: empty 4-bit register receiving 1, 0, 1, 1 → `0001`, `0010`, `0101`, `1011`.
- **Shift register + counter = a serial receiver.** This is the core of K5.

## Mistakes I made
- Said a 0–15 counter needs 5 flip-flops. It needs 4: the top value is 15 = `1111`; it wraps instead of reaching 16.

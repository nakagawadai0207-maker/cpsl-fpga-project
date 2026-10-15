# K5. The whole serial link in simulation

**Where it sits:** the K4 transmitter and receiver, connected and tested on the laptop (EDA Playground / Icarus) before any hardware. Then a read-through of a real 1 MHz PMOD loopback module, to see what a working on-board version adds. Done 2026-10-15.

## The link
- Testbench: makes a clock (`always #5 clk = ~clk;` gives a 10 ns period), wires the transmitter's `dout` to the receiver's `din`, and shares one `frame` wire. Instances use `.port(wire)`.
- Result: `word = 10110010` (EPWave shows hex **b2**) at 165 ns, the 17th rising edge. Edges 1 to 8 send the starting zeros, the byte loads at edge 8, edges 9 to 16 carry its bits, and edge 17 latches it.
- Code: [link.v](../dca1000-removal/code/k5/link.v), [tb.v](../dca1000-removal/code/k5/tb.v).

## Break it: data late, frame on time
Put one flip-flop in the data path (`link_late <= link`) but leave `frame` alone.

| Delay | `word` | hex | Why |
|---|---|---|---|
| 0 | `10110010` | b2 | correct |
| 1 clock | `01100101` | 65 | rx holds b6…b0 of this byte + b7 of the **previous** byte |
| 2 clocks | `11001010` | ca | b5…b0 + previous byte's b7, b6 |

- The first latch with 1 clock of delay gives `01100100` (64), because the "previous byte" was the starting zeros.
- The receiver can't tell anything is wrong. This is the **bit-alignment** problem; on the radar's LVDS lanes it's solved with the frame clock and by moving the sample point (K9).

## A real on-board version: what it adds
Same receive line as K4, 32 bits wide. Three new ideas:

1. **Many clocks per bit, sampled in the middle.** At 200 MHz with 200 clocks per bit (1 Mb/s), a counter counts the clocks inside each bit (0 to 199). The input is read once, at count 100; the output moves to the next bit at count 199. A second counter counts bits (0 to 31).
   - The data can arrive up to about 100 clocks (half a bit) late and still be read correctly. My K5 design has 1-clock bits, so 1 clock of delay breaks it.
   - The middle is safest because of physical effects: wire and pin delay, edges that take time to switch, and (between two boards) slightly different clocks.
   - One 32-bit word takes 32 × 200 = 6,400 clocks = **32 µs** to send.
   - The radar's ~600 Mb/s lanes have bits shorter than one 5 ns clock, so this counting method can't work there. That's why the radar sends its own clock (K9).
2. **A state machine.** A register `state` says which step the module is on, and on each clock only that step's code runs:
   - **IDLE:** wait until a word is offered, then copy it in and reset the counters.
   - **SHIFT:** send the 32 bits on the output pin and read each one back.
   - **OUTPUT:** offer the rebuilt word to the next block, and wait until it's taken.
3. **The AXI-Stream handshake** between blocks: `tdata` (the word), `tvalid` (sender: "this is a real word"), `tready` (receiver: "I can take it"), `tlast` (last word of a packet). A word moves only on a clock where `tvalid` and `tready` are both 1; otherwise the sender holds it. If the next block keeps `tready` at 0, the module waits in OUTPUT and doesn't take a new word, so the one before it waits too (**backpressure**). This is the interface the LVDS receiver will need to feed the DMA (K10).

## Mistakes I made
- Thought `link` turning on was caused by `frame` dropping. It's coincidence: bit 0 of the byte is 0.
- Thought `frame` is high when `bitcnt` = 111. It's high at 000.
- EDA Playground errors: forgot the `.` in `.din(link)`, forgot the `input wire din` port, wrote `$b` instead of `%b`.
- Called the clocks-in-a-bit counter "the counter the frame uses". It counts clocks inside one bit; the bit counter (0 to 31) is the one that marks the end of a word.
- Said "half a tick". One tick is one clock and can't be split; the sample is half a **bit** in.
- Multiplied 6,400 ticks × 5 ns and called the result "ticks". That's 32,000 ns = 32 µs of time.

# K4 (part 1). Just enough Verilog for the first lab

**Where it sits:** this is the code that goes onto the board on the first lab visit. The rest of K4 (more Verilog, HDLBits) comes before K5.

## Verilog describes hardware
- It isn't a list of steps run in order. Each line describes a part (flip-flops, an adder, a wire), and all parts run at the same time.

## Pieces
- `module name ( ports ); … endmodule`: one named block of hardware.
- **Ports:** `input` comes in, `output` goes out.
- `reg [26:0] count = 0;`: 27 flip-flops, bits 26 down to 0, starting at 0.
  - `[15:0]` = 16 flip-flops; highest **bit number** 15; highest **value** 2¹⁶ − 1 = 65,535.
- `always @(posedge clk) begin … end`: runs at every rising edge. Anything assigned here becomes **flip-flops**.
- `count <= count + 1;`: `count + 1` is an **adder**. `<=` = use the values from just before the edge, then update everything at once.
  - `a <= b; b <= a;` swaps a and b each edge (3, 5 → 5, 3).
  - `count <= count + 2` from 0: 2, 4, 6, 8.
- `assign led = count[26];`: a permanent **wire**, no clock.

| | Updates when | Hardware |
|---|---|---|
| `always @(posedge clk)` with `<=` | only at rising edges | flip-flops |
| `assign` | continuously | wires / logic |

## Code
- [blink.v](code/blink.v)
- [loopback.v](code/loopback.v) (I wrote the two `assign` lines)

## Mistakes I made
- Said the highest bit number of `[15:0]` is 2¹⁶ − 1. That's the highest *value*; the highest bit *number* is 15.
- (2026-10-13, writing loopback.v myself) Declared the counter as `[25:0]` when I needed bit 26. The left number is the highest bit *used*, so `[26:0]` = 27 flip-flops.
- Typed `podedge` and kept the example's signal name `tick` instead of my port `clk`.
- Wrote `in_pin[0]`: you can't index a 1-bit wire; just `in_pin`. Forgot `endmodule`.

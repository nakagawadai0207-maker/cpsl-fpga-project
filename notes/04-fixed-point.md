# Lesson 4: numbers in hardware (fixed point)

## Why FPGAs use integers
- The ADC already outputs integers (14-bit samples).
- The speed comes from **parallelism**. A CPU core does multiplies mostly one after another, while the K26 has 1,248 DSP slices that each do a multiply every clock, all at once.
- Integers keep each multiplier small, so more fit on the chip. A float add needs extra hardware to compare exponents, shift to line them up, add, and then renormalize. An integer add is just the add.

## Two's complement (8-bit shown; 16-bit works the same)
- Bit weights: **−128**, 64, 32, 16, 8, 4, 2, 1. Only the top bit is negative.
- To negate: flip all the bits, then add 1. Example: 5 = `0000 0101`, so −5 = `1111 1011`.
- int16 range: −32,768 to +32,767.
- Overflow is **silent**: 127 + 1 = `1000 0000` = −128. You get no error, just garbage.

## Q1.15 fixed point
- stored integer = value × 32,768. Range is −1 to 0.99997 (+1.0 would need 32,768, one past the int16 max).
- 0.5 → 16,384, −0.5 → −16,384, 0.75 → 24,576.
- **Add:** add the integers directly (both are on the same scale). This can overflow: 0.75 + 0.75 wraps to −0.5.
- **Multiply:** multiply the integers, then divide by 32,768, which is the same as chopping the lowest 15 bits. In hardware this is free: you just don't wire the low 15 bits.
  - 0.75 × −0.5: 24,576 × −16,384 = −402,653,184 → chop 15 bits → −12,288 = −0.375
- Chopping is for re-scaling *after a multiply*. Reading a value back means dividing by 32,768, which Python does.

## Data flow
Integers from the ADC go to the FPGA, which does lots of integer math in parallel. The integer results are copied by DMA to DDR memory. Python then divides by 32,768 only if it needs the real values; finding the biggest peak doesn't need that step.

## Overflow in the FFT
- Each FFT output is a sum of N products. For a perfectly matched tone, output = N × input. In radar this is normal, because a strong target puts all its energy into one output.
- 4-point example with samples of 0.5. Adding in two stages gives 0.5+0.5 = 1.0, then 1.0+1.0 = 2.0, which overflows. Dividing by 2 after each stage keeps every value at 0.5, so the output is 4× smaller than the true answer, and Python multiplies by 4 to get it back.
- **Leftover growth = FFT size ÷ total division. Max input = 1 ÷ leftover growth.**
  - Lab FPGA FFT: 256-point with ÷16 total (÷2 at each of its 4 radix-4 stages, per `fpga_fft.py`). That leaves 16× growth, so inputs must stay under 1/16 (about 2,048), and Python multiplies the output by 16.
  - 1024-point with ÷32 → 32× → inputs under 1/32 (about 1,024).
- **The price of dividing:** each ÷2 chops off a bit. A weak target whose true output is 40 becomes 0 after ÷64, and multiplying back can't recover it. This is the core fixed-point trade-off: divide too little and you overflow; divide too much and weak signals vanish.

## Mistakes I made
- Said "chop 15 bits" to read 24,576's value. Chopping gives 0; reading a value means dividing.
- Thought the FPGA is faster *because* integers are cheap. The speed comes from parallelism; cheap integers are what allow that much parallelism.
- Added in the stage-1 values wrong (got 1.5 instead of 1.0).
- Mixed the input value into the leftover-growth calculation. Leftover growth depends only on FFT size ÷ division.

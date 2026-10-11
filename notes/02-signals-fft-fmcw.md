# Lesson 2: signals, the FFT, and FMCW radar

## Start from the physical thing
An FMCW radar's raw output, after mixing, is a **tone**. Its **pitch (frequency) tells you the distance**: a farther target gives a higher pitch. Everything below is just about measuring that pitch.

## Complex numbers (I/Q)
- The radar samples two channels, I and Q, which together form a complex number `a + bj`.
- **Magnitude** = √(a² + b²), by Pythagoras, *not* cos/sin. Example: |5 + 12j| = √(25 + 144) = 13.
- Multiplying a complex number by itself squares its length and doubles its angle.

## FFT = a bank of tuning dials
For each test frequency, multiply the signal by a reference tone at that frequency and add up the result. If the signal contains that frequency, the products line up and the sum is big. If it doesn't, they cancel out.

The output is a **spectrum**: loudness vs. frequency, which for radar means loudness vs. distance. A target shows up as a spike, and a farther target moves its spike to the right.

## FMCW chirp → beat frequency
- The transmitter sweeps frequency upward (a chirp). In the lab setup the slope is **80 MHz/µs**.
- The echo comes back delayed, so at any instant it's at a slightly lower frequency than what's being sent. Mixing the two gives a **beat frequency**, which is proportional to distance.
- Beat frequency = slope × 2d / c. For 1 m that's 80e12 × 2 / 3e8 ≈ **533 kHz**. For 2 m it doubles to about 1.07 MHz.

## Range resolution
- Δd = c / (2B), where B is the bandwidth swept by the chirp.
- B = 2.4 GHz gives **6.25 cm**. Doubling B *halves* this, which is finer resolution.

## Mistakes I made
- Used cos/sin to get a magnitude. Magnitude is just Pythagoras.
- Forgot that a farther target also means the spike moves right on the spectrum.
- Said doubling bandwidth doubles the resolution number. It halves it.

# Lesson 3: break the radar on purpose

Script: [`code/lesson3.py`](../code/lesson3.py). Run it from the lab's radar Python folder, since it imports that folder's `radar_config`, `radar_fft` and `synthetic_radar` modules.

## Two facts
- **Max range ≈ 3.93 m** for this configuration. Past that, the beat frequency is higher than the sampling can represent.
- **FFT size = how many test pitches** the FFT tries.

## Experiments (predict first, then run)
- **A.** Put a target at 4.5 m. What happens?
- **B.** Put two targets 4 cm apart (1.00 m and 1.04 m). Do you see two peaks at FFT size 64? At 1024?
- **C.** Put two targets 20 cm apart (1.0 m and 1.2 m) at FFT size 256.

## Aliasing (needed for A)
The ADC samples the beat tone at a fixed rate, like seeing a spinning fan only under a strobe light. A fan turning 1.25 turns/sec looks exactly like one at 0.25 turns/sec. In the same way, the distance axis **wraps around at 3.93 m**. A target past the limit shows up at (distance − 3.93), and nothing in the plot warns you. A target under the limit shows up where it really is.

Warm-up: 2.0 m → 2.0 m (under the limit, no wrap); 5.0 m → 1.07 m.

## My predictions
- **A:** 4.5 − 3.93 = 0.57 m. Ran it: peak at 0.57 m ✅
- **B:** one peak at both 64 and 1024. 4 cm < 6.25 cm, and FFT size doesn't change resolution.
- **C:** two peaks, since 20 cm > 6.25 cm.

## What FFT size actually is
1. Each chirp gives the ADC 63 samples. That's all the information there is.
2. The FFT checks a list of test pitches (each pitch = a distance) against those samples.
3. FFT size = how many test pitches, spread evenly from 0 to 3.93 m: 64 → one every 6.1 cm, 1024 → one every 0.4 cm. The extra slots are zero-padding, which adds no information.
4. The recording is short, so each target makes a peak about c/2B ≈ 6.25 cm wide, whatever the FFT size. A bigger FFT draws the same peak with more dots: smoother, not wider.

**Where FFT size does matter:**
- Reading a peak's position. C at 64 gives 0.984 / 1.168 m; at 1024 it gives 1.003 / 1.199 m.
- Borderline gaps. 10 cm apart shows one peak at 64 and two at 1024, because no test pitch landed in the dip between them.
- Hardware cost. 1024 points needs ~16× the memory of 64, plus far more multiplies. On an FPGA, pick the smallest size that's precise enough.

ADC sample rate is a different knob: it sets the max range (3.93 m), not the resolution.

## What actually happened
_TBD_

## Mistakes I made
- Subtracted 3.93 from a target that was already under the limit (2.0 m). Only wrap when distance > 3.93 m.
- Thought a bigger FFT makes the peak wider. It makes it smoother; the width is set by bandwidth.

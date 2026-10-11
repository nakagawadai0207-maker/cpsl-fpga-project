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
- **B:** _TBD_
- **C:** _TBD_

## What actually happened
_TBD_

## Mistakes I made
- Subtracted 3.93 from a target that was already under the limit (2.0 m). Only wrap when distance > 3.93 m.

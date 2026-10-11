# Lesson 3: break the radar on purpose

Script: [`code/lesson3.py`](../code/lesson3.py). Run it from the lab's radar Python folder, since it imports that folder's `radar_config`, `radar_fft` and `synthetic_radar` modules.

## Two facts
- **Max range ≈ 3.93 m** for this configuration. Past that, the beat frequency is higher than the sampling can represent.
- **FFT size = how many test pitches** the FFT tries.

## Experiments (predict first, then run)
- **A.** Put a target at 4.5 m. What happens?
- **B.** Put two targets 4 cm apart (1.00 m and 1.04 m). Do you see two peaks at FFT size 64? At 1024?
- **C.** Put two targets 20 cm apart (1.0 m and 1.2 m) at FFT size 256.

## My predictions
_TBD_

## What actually happened
_TBD_

# Lesson 3: break the radar on purpose. Edit the TARGETS and N_FFT lines, then run.
import numpy as np
import matplotlib.pyplot as plt
import radar_config as cfg
import radar_fft as rf
from synthetic_radar import Target, generate_frame

TARGETS = [Target(1.0, 0.0, 0.0)]   # (distance in m, speed, angle) -- only distance matters today
N_FFT = 64                          # FFT size
WINDOW = True

cube = generate_frame(TARGETS, noise_std=0.0)
spec = np.abs(rf.range_fft(cube, n_fft=N_FFT, window=WINDOW))[0, :, 0]   # RX 0, chirp 0
dist = cfg.range_axis(N_FFT)
plt.plot(dist, spec)
plt.xlabel("distance (m)"); plt.ylabel("loudness"); plt.title(f"spectrum, FFT size {N_FFT}")
plt.show()

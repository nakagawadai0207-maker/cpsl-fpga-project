# Radar

**Goal:** understand how the lab's FMCW mmWave radar turns reflections into distances, well enough to follow the lab's research and to know what the FPGA work has to process.

## Notes
- [Lesson 2: signals, the FFT, and FMCW radar](notes/02-signals-fft-fmcw.md): complex (I/Q) samples, the FFT, chirp → beat frequency, range resolution
- [Lesson 3: break the radar on purpose](notes/03-fft-experiments.md): aliasing, resolution vs. FFT size, choosing an FFT size ([script](code/lesson3.py))

## Reading
- TI, *Introduction to mmWave Sensing: FMCW Radars* (Sandeep Rao): slide deck, in progress

## Where this connects
- The radar's raw samples leave the chip over LVDS, which is what the [DCA1000 removal](../dca1000-removal/) work receives.
- The FFT from Lessons 2–3 is the first computation to [hardware-accelerate](../fpga-acceleration/).

# My work at CPSL

I'm an undergraduate research assistant at Duke University's Cyber-Physical Systems Lab (CPSL), working on FMCW mmWave radar. This repo documents what I work on there and what I learn along the way, starting from zero.

## Three sections

| Section | What it is | Status |
|---|---|---|
| [**Radar**](radar/) | Learning how FMCW mmWave radar works: chirps, beat frequency, the FFT, range resolution | Lessons 2–3 done |
| [**DCA1000 removal**](dca1000-removal/) | **My main contribution to the lab.** Replace the DCA1000 capture board so the radar's LVDS data goes straight into an AMD Kria FPGA board | Current focus: first design running on the board |
| [**FPGA and hardware acceleration**](fpga-acceleration/) | For my future: how an FPGA fits into a whole system (pins → logic → AXI bus → memory → software), and how to move a heavy computation into hardware | Lessons 1 and 4 done |

The sections overlap on purpose: removing the DCA1000 needs FPGA skills, and the FPGA work exists to process radar data.

**[lessons/](lessons/)** holds every lesson in one sequence, in my own words, with a "Mistakes I made" section. Lessons aren't tied to one section: each pulls from whatever topic it needs, and the section pages summarize what I've learned for that area.

[**PROGRESS.md**](PROGRESS.md) has progress bars for each section and a dated log of everything. Lab-internal code and documents are kept out of this repo.

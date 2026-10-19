import numpy as np

# Fake radar frame: every value equals its own position in the radar's order (chirp, rx, sample).
radar = np.arange(52920)
radar = radar.reshape(210, 4, 63)

# The bridge: reorder into Person A's order (rx, sample, chirp) and really move the data.
cube = radar.transpose(1, 2, 0)
cube = np.ascontiguousarray(cube)

flat = cube.reshape(-1)
# flat[13655] = 1262   # uncomment to fake a bridge bug

ok = True

for p in range(52920):
    chirp = p % 210
    sample = p // 210 % 63
    rx = p // 210 // 63
    expected = chirp * 252 + rx * 63 + sample
    if flat[p] != expected:
        print("WRONG at", p, "rx", rx, "sample", sample, "chirp", chirp, "got", flat[p], "expected", expected)
        ok = False
        break

if ok:
    print("PASS")

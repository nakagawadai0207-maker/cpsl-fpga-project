import numpy as np

radar = np.zeros((210, 4, 63, 2), dtype=np.int16)
for c in range(210):
	for r in range(4):
		for s in range(63):
			radar[c, r, s, 0] = s
			radar[c, r, s, 1] = r * 1000 + c
print(radar[5, 1, 2])

cube = np.ascontiguousarray(radar.transpose(1, 2, 0, 3))

print(cube[1, 2, 5])

# cube[1, 2, 5, 1] = 1   # uncomment to plant a bug
ok = True

for r in range(4):
	for s in range(63):
		for c in range(210):
			if (cube[r, s, c, 0] != s ) | (cube[r, s, c, 1] != (1000 * r + c)):
				ok = False
				print("WRONG at rx", r, "sample", s, "chirp", c, "got", cube[r, s, c])
				break

if ok:
	print("PASS")

words = cube.view(np.int32)   # same bytes, read as the 32-bit words the DMA sees
print(words[1, 2, 5])         # Q * 65536 + I = 1005 * 65536 + 2 = 65863682

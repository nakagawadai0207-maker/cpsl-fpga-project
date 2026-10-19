import numpy as np

radar = np.arange(52920)
radar = radar.reshape(210, 4, 63)
print(radar[5, 1, 2])
cube = radar.transpose(1, 2, 0)
print(cube[1, 2, 5])

cube = np.ascontiguousarray(cube)
print(cube.reshape(-1)[13655])
print(cube.reshape(-1)[0:3])

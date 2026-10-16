# K10: counter_stream -> AXI DMA (S2MM) -> DDR, checked from Python (PYNQ).
# Needs k10_dma.bit and k10_dma.hwh in the same folder (names must match).
# Ran on the KR260 2026-10-16: printed [0 1 2 3 4 5 6 7] and True.
from pynq import Overlay, allocate
import numpy as np

ol = Overlay("/home/ubuntu/dai/k10_dma.bit")   # load into the PL; reads k10_dma.hwh next to it
dma = ol.axi_dma_0               # handle to the DMA (registers at 0xA000_0000)

buf = allocate(shape=(1024,), dtype=np.uint32)   # 1024 x 32-bit slots in DDR

dma.recvchannel.transfer(buf)    # S2MM: write ADDRESS, then LENGTH (= go)
dma.recvchannel.wait()           # poll STATUS until done (tlast ends the packet)

print(buf[0:8])                                  # expect [0 1 2 3 4 5 6 7]
print(np.array_equal(buf, np.arange(1024)))      # expect True

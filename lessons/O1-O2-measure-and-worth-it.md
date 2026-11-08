# O1–O2: Measure the path, and is speeding it up worth it?

Part of the [Ethernet demo](../ethernet-demo/) ([plan](../ethernet-demo/PLAN.md)). Done 2026-11-07.

## O1: Timing decode on its own

I wrote `time_decode.py` on the Kria. It:
1. imports the lab's decode function (`from <file> import <function>`, with no `.py`)
2. makes one fake raw frame, 211,680 random bytes: `np.random.randint(0, 256, 211680, dtype=np.uint8).tobytes()`
3. times 100 decodes with `time.perf_counter()` and prints `(t1 - t0) * 1000 / 100`, the ms per decode

Random bytes are fine, because decode does the same work whatever the values are.

**Result: about 5.5 ms per decode** on the ARM. Other software was running on the board at the same time, so this may be a little high. Decode turned out to be roughly 40% of the whole Ethernet → map path.

## O2: Is it worth it?

- **Frame budget = 1000 / fps.** At 20 fps a new frame arrives every 50 ms, and the path uses only about a quarter of that. The Kria is idle the rest of the time.
- **A faster Kria doesn't make more frames.** The radar's config file sets the frame rate. Faster processing only makes the Kria wait longer, or shortens the delay to the screen.
- **The frame rate can be raised in the config.** At about 91 fps the budget is about 11 ms per frame. At that rate the path doesn't fit: packet capture in Python gets slower as packets per second rise.
- **Cutting decode alone isn't enough at 91 fps.** Capture (receiving the packets) is the other big cost.

| Option | Capture done by | Decode done by |
|---|---|---|
| now | ARM (Python) | ARM (Python) |
| software shortcut | ARM (Python) | ARM, faster |
| reorder in fabric | ARM (Python) | fabric |
| Ethernet in fabric | fabric | fabric |

Only Ethernet in the fabric removes both steps from the ARM. On paper that's enough for 91 fps, but it's a large HDL project. The cheaper first try is to **split capture and processing across the ARM's 4 cores**. This has to use separate processes, because Python threads can't run Python code at the same time (the GIL).

**Conclusion:** at 20 fps, not worth it. At higher frame rates: try the 4-core split first, and Ethernet in the fabric only if the split isn't enough. My mentor said 20 fps is enough for his project; higher rates are an optional exploration (see the [frame-rate experiment](O-frame-rate-experiment.md)).

## Mistakes I made
- `from dca1000.py import ...`: an import never includes `.py`
- forgot `time.perf_counter()`, and the colon at the end of a `for` line
- forgot to divide by 100 to get the time per run
- set up the share upside down at first (whole / part instead of part / whole)
- treated "+10.8 ms per frame" as a cost per extra fps
- first picked the software option as the one that removes both steps; it keeps capture on the ARM

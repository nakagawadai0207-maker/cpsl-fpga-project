# Lab day 1: blink and loopback on one KR260

**Goals, in order:**
1. Open Vivado on the lab PC (last box on the "Ready for the lab" bar).
2. Load **your own Verilog** onto the Kria and see an LED blink.
3. Add one jumper wire and watch the LED follow it.

**Your design:** [`code/kria-link/loopback.v`](../code/kria-link/loopback.v). It already contains the blink (bit 26 of the counter goes out on `out_pin`).

Where these steps come from: the lab's own docs in `CPSL_Manuals/Kria Board` (QUICKSTART, the template project, `projects/pmod-serial-loopback`). Those docs were AI-written, so the multimeter check in step 7 is not optional.

---

## 0. Ask when you arrive (Person B or David)
- Which KR260 can I use, and what is its **IP address**?
- Is PYNQ installed on it?
- Is the template project at `/home/cpsl/kria_board_template_new/` and are the scripts (`kria_new_project.sh`, `kria_build_deploy.sh`) on the lab PC?

## 1. Check the board is healthy (lab PC terminal)
```bash
python3 scripts/board/check_board_status.py --host <kria_ip>
```
Every line should say PASS (two need root; the doc says that's expected).

## 2. Make your project from the lab template
```bash
./scripts/host/kria_new_project.sh dai_loopback
vivado /home/cpsl/dai_loopback/dai_loopback.xpr &
```
Vivado opening = **last box on the lab bar ticked.**

## 3. Add your Verilog
1. Sources panel → **+** → **Add or Create Design Sources** → **Add Files** → `loopback.v`
2. Tick **Copy sources into project** → **Finish**

## 4. Put it in the block design
1. Open the block design (Sources → Design Sources → `kria_board_template`).
2. Right-click the canvas → **Add Module** (not Add IP) → `loopback`.
3. Wire `clk_wiz_0` **clk_out1** → `loopback_0` **clk**.
4. **Write down clk_out1's frequency** (double-click `clk_wiz_0`). The lab's DMA project uses 200 MHz.
   - **Predict before building:** at 200 MHz, bit 26 flips every 2²⁶ ÷ 200×10⁶ ≈ **0.34 s**. At 100 MHz, ≈ 0.67 s.
5. Right-click `out_pin` → **Make External**. Same for `in_pin` and `led`.
6. Rename each external port to exactly `out_pin`, `in_pin`, `led` (Vivado adds `_0`; the XDC names must match).
7. Press **F6** (validate). DMA interrupt warnings are expected and harmless.

## 5. Tell Vivado which physical pins (XDC)
Add to the project's `.xdc` file (don't delete anything):
```tcl
# ---- Dai loopback test, PMOD 4 upper row, single-ended 3.3 V ----
set_property PACKAGE_PIN AC12 [get_ports {led}]       ;# PMOD4 pin 1 -> external LED
set_property IOSTANDARD LVCMOS33 [get_ports {led}]
set_property PACKAGE_PIN AD12 [get_ports {out_pin}]   ;# PMOD4 pin 3 -> jumper
set_property IOSTANDARD LVCMOS33 [get_ports {out_pin}]
set_property PACKAGE_PIN AF10 [get_ports {in_pin}]    ;# PMOD4 pin 7 <- jumper
set_property IOSTANDARD LVCMOS33 [get_ports {in_pin}]
set_property PULLDOWN TRUE [get_ports {in_pin}]       ;# reads 0 when the wire is pulled
```
These pin numbers are from the lab's template XDC (PMOD 4 upper row: AC12, AD12, AE10, AF10) and match the lab's own loopback project.

## 6. Build and send it to the Kria (about 7 minutes per the lab doc)
```bash
./scripts/host/kria_build_deploy.sh /home/cpsl/dai_loopback/dai_loopback.xpr --host <kria_ip>
```
Expected noise: lots of `cannot add Board Part` warnings. Real problems: **"No ports matched"** (a port name doesn't match the XDC) or a **DRC error** on a pin.

## 7. Wire it (with nothing loaded: `sudo xmutil unloadapp` on the Kria first)
PMOD 4 upper row, per the lab doc (viewed from above):
```
pin11   pin9   pin7    pin5    pin3    pin1
3.3V    GND    AF10    AE10    AD12    AC12
               in_pin  (free)  out_pin led
```
1. **Multimeter first:** find pin 11 (should read 3.3 V) and pin 9 (GND) so you know the row is oriented the way you think.
2. **LED:** pin 1 → 330 Ω resistor → LED **long leg**; LED **short leg** → pin 9 (GND).
3. **Jumper:** pin 3 → pin 7.

## 8. Run it (on the Kria)
```bash
cd ~/my_overlays/dai_loopback
./run_bitstream.sh
```
This loads the overlay. Your design then runs on its own; Python doesn't control it.

## 9. Predict, then test (write predictions down first)
| Test | Prediction | What you saw |
|---|---|---|
| Jumper in place | LED blinks at the rate from step 4 | |
| Pull the jumper | LED off (pulldown makes `in_pin` read 0) | |
| Jumper from pin 7 to pin 11 (3.3 V) | LED on, steady | |
| Jumper from pin 7 to pin 9 (GND) | LED off | |

**Never** touch pin 3 (`out_pin`) to 3.3 V or GND: it's an output, and that shorts it.

## 10. Finish
```bash
sudo xmutil unloadapp
```
Commit your `.xdc` changes and a photo or note of what happened to the GitHub journal.

## If something goes wrong
| Symptom | Likely cause |
|---|---|
| "No ports matched" warning | External port names don't match the XDC (check for `_0`) |
| LED never lights, even with pin 7 → 3.3 V | LED backwards (swap legs), or wrong pin row |
| LED stuck on/off with jumper in place | `clk` not connected to `clk_wiz_0`, or clock wizard held in reset |
| `Overlay()` hangs | PL lock held: `sudo xmutil unloadapp` |

## Things to ask while you're there
- (For Person B) Two KR260s over PMOD single-ended, or the custom carrier for real LVDS?
- (For Person A) "Remove Vivado": PYNQ with a prebuilt bitstream, or something else?
- Are `LED1` (AH17) / `LED2` (AF17) in the template XDC the on-board user LEDs?

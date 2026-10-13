# Lab day 1, laptop version: build `loopback.v` on Windows, load it with `xmutil`

Why this version exists: there is no lab PC, and this KR260 has no PYNQ (checked 2026-10-13).
So Vivado runs on the laptop, and the board loads the design with AMD's own loader, `xmutil`.

Wiring (done and checked 2026-10-13): PMOD4 pin 1 → 330 Ω → LED → pin 9 (GND); jumper pin 3 → pin 7.
Pin map confirmed with a multimeter (pin 11 = +3.33 V vs pin 9) and against a
[Hackster KR260 PMOD4 project](https://hackster.io/iotengineer22/control-gpio-from-pynq-and-kr260-0d3613)
(pin 1 = AC12, pin 3 = AD12, pin 7 = AF10).

## What the board needs

`xmutil loadapp <name>` loads three files from `/lib/firmware/xilinx/<name>/`:

| File | What it is | Where it comes from |
|---|---|---|
| `dai_loopback.bit.bin` | the bitstream | Vivado (step 9 below) |
| `dai_loopback.dtbo` | device tree overlay: names the bitstream and turns on `pl_clk0` (100 MHz) | [`code/kria-link/firmware/`](../code/kria-link/firmware/) (already built) |
| `shell.json` | tells `xmutil` it's a plain full-PL design | [`code/kria-link/firmware/`](../code/kria-link/firmware/) |

The overlay follows AMD's own pattern in [kria-apps-firmware](https://github.com/Xilinx/kria-apps-firmware)
(`boards/kr260/bist/kr260-bist.dtsi`, `k26-dfx/2rp/opendfx_shell_wrapper.dtsi`).

## Vivado steps (2025.2, Windows)

1. **Create Project.** Name `dai_loopback`, location `C:\fpga` (no spaces in the path).
   RTL Project, tick "Do not specify sources at this time".
2. **Part/board:** Boards tab, search `KR260`, pick **Kria KR260 Robotics Starter Kit**.
   If it isn't listed, click the refresh/download button (needs Wi-Fi). Finish.
3. **Add the Verilog:** Add Sources → design sources → add `loopback.v`.
4. **Block design:** Create Block Design (`design_1`). Add IP → **Zynq UltraScale+ MPSoC**.
   Click **Run Block Automation** → OK (applies the KR260 preset).
5. **Trim the Zynq block:** double-click it → PS-PL Configuration → PS-PL Interfaces → Master Interface:
   untick every AXI HPM master. (This design doesn't use AXI, and unconnected masters cause validation errors.)
   Clock Configuration → Output Clocks → PL Fabric Clocks: leave **PL0 at 100 MHz** ticked. OK.
6. **Add your module:** right-click the canvas → **Add Module** → `loopback`. Drag a wire from `pl_clk0` to `clk`.
7. **Pins out:** right-click `led` → Make External. Same for `out_pin` and `in_pin`.
   Rename each external port to exactly `led`, `out_pin`, `in_pin` (delete the `_0`).
8. **Validate** (F6). In Sources, right-click `design_1` → **Create HDL Wrapper** → let Vivado manage it.
9. **Constraints:** Add Sources → constraints → create `pins.xdc`, paste:
   ```tcl
   set_property PACKAGE_PIN AC12 [get_ports {led}]       ;# PMOD4 pin 1
   set_property IOSTANDARD LVCMOS33 [get_ports {led}]
   set_property PACKAGE_PIN AD12 [get_ports {out_pin}]   ;# PMOD4 pin 3
   set_property IOSTANDARD LVCMOS33 [get_ports {out_pin}]
   set_property PACKAGE_PIN AF10 [get_ports {in_pin}]    ;# PMOD4 pin 7
   set_property IOSTANDARD LVCMOS33 [get_ports {in_pin}]
   set_property PULLDOWN TRUE [get_ports {in_pin}]
   ```
10. **Make a .bin too:** Settings → Bitstream → tick **-bin_file**.
11. **Generate Bitstream.** When it finishes, the file is
    `C:\fpga\dai_loopback\dai_loopback.runs\impl_1\design_1_wrapper.bin`.
    Copy it next to the other two files and rename it **`dai_loopback.bit.bin`**.
    If there's no `.bin` (forgot `-bin_file`), don't rebuild: Open Implemented Design, then in the Tcl Console
    `write_bitstream -force -bin_file C:/fpga/load/dai_loopback.bit` and rename `dai_loopback.bin`.
    The `.bit.bin` is 136 bytes smaller than the `.bit` (the header). Worked first try on 2026-10-13.

## Copy to the board and load (laptop on wired Ethernet)

In PowerShell, from the folder holding the three files:
```
scp dai_loopback.bit.bin dai_loopback.dtbo shell.json ubuntu@10.147.192.102:~/dai/
ssh ubuntu@10.147.192.102
```
On the board:
```
sudo mkdir -p /lib/firmware/xilinx/dai_loopback
sudo cp ~/dai/dai_loopback.bit.bin ~/dai/dai_loopback.dtbo ~/dai/shell.json /lib/firmware/xilinx/dai_loopback/
sudo xmutil listapps
sudo xmutil unloadapp
sudo xmutil loadapp dai_loopback
```

## Tests

| Wiring | Expected |
|---|---|
| Jumper pin 3 → pin 7 | LED blinks, ~0.67 s on / 0.67 s off (bit 26 at 100 MHz) |
| Pull the jumper out of pin 7 | LED off (pulldown) |

## Undo (puts the board back the way it was)

```
sudo xmutil unloadapp
sudo xmutil loadapp k26-starter-kits
sudo rm -r /lib/firmware/xilinx/dai_loopback
```
A reboot also reloads the default `k26-starter-kits` design.

## If it goes wrong

| Symptom | Likely cause |
|---|---|
| `loadapp` error | file names don't match `firmware-name` in the overlay (`dai_loopback.bit.bin`), or files not in `/lib/firmware/xilinx/dai_loopback/` |
| Loads, LED never blinks | `pl_clk0` not wired to `clk`, or a port name doesn't match the XDC ("No ports matched" warning in Vivado) |
| Fan gets loud | the template drove the fan pin from the PL and this design doesn't; expected, not harmful (inference, check with Person B) |

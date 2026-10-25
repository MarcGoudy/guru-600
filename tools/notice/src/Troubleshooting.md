# If the FM-1 does not start

If an update is interrupted and the FM-1 stays black, check whether a computer sees it as a USB device named
**WL80UBOOT** (or a USB mass-storage device with ID 4C4A:8057). That is the chip's built-in boot mode, and
the FM-1 can be brought back:

- First try another USB data cable, and close every other app that uses MIDI, then run the web installer again.
- If it stays in boot mode, [FM-1 Transporter](https://github.com/kurogedelic/FM-1-transporter) reads and
  writes the FM-1's flash from a Mac through a Seeed XIAO RP2040 (three wires to the FM-1's USB lines). Back up
  the flash first, then write the official firmware (M-VAVE's FM-1.fwsc).
- Questions: [Issues](https://github.com/hugelton/Felucca/issues).

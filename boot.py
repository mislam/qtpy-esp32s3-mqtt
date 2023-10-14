# boot.py runs only after a hard reset.

# The CIRCUITPY storage drive is normally visible on the host computer.
# Uncomment the following two lines to disable it from mounting as a USB device.
# Once disabled, to mount the storage drive, press the RESET button and wait
# until for yellow flashs after purple. Then immediately press the BOOT button.
import storage

storage.disable_usb_drive()

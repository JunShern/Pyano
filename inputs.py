from evdev import InputDevice, list_devices, categorize, ecodes
from select import select
import sys

orig_stdout = sys.stdout
f = file('out.txt', 'w')
sys.stdout = f

## Input Devices
devices = list()
for fn in list_devices():
    dev = InputDevice(fn)
    if "eyboard" in dev.name:
        print dev
        devices.append(dev.fn)

devices = map(InputDevice, devices) 
devices = {dev.fd: dev for dev in devices}
    
count = 1
while True:
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            if event.type == ecodes.EV_KEY and event.value == 0:
                ## Check for quit
                if ecodes.KEY[event.code] == "KEY_ESC":
                    sys.stdout = orig_stdout
                    f.close()
                    sys.exit()

                print ecodes.KEY[event.code], count
                #print devices[fd].name, ecodes.KEY[event.code], event.value
                count += 1


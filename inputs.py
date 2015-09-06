from evdev import InputDevice, list_devices, categorize, ecodes
from select import select

devices = list()
for fn in list_devices():
    dev = InputDevice(fn)
    if "eyboard" in dev.name:
        print dev
        devices.append(dev.fn)

devices = map(InputDevice, devices) 
devices = {dev.fd: dev for dev in devices}
    
while True:
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            if event.type == ecodes.EV_KEY and event.value != 2:
                print devices[fd].name, ecodes.KEY[event.code], event.value

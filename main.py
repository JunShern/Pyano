import sys
import time
import keyboard
import midi as md
import display 
from helpers import *
from memory import *
from evdev import InputDevice, list_devices, categorize, ecodes
from select import select

midi = md.Midi()
midi.setup()
disp = display.Display()
disp.setup(fullscreen=0)

## Memory setup
mem = 1
inst_mem = list()
base_mem = list()
vol_mem = list()
vel_mem = list()
readMemory(inst_mem, base_mem, vol_mem, vel_mem)
print "Memory setup OK!"

## Getting devices
devices = list()
for fn in list_devices():
    dev = InputDevice(fn)
    rate = dev.repeat[0] # Extract keyboard repeat rate 
    if rate > 0: ## Will be zero unless it's a keyboard! :)
        print dev
        devices.append(dev.fn)

devices = map(InputDevice, devices) 
devices = {dev.fd: dev for dev in devices}
num_devices = len(devices)
print num_devices, "keyboards detected."
if num_devices == 0:
    print "Please ensure that you are root, and that you have keyboards connected."
    print " "
    disp.close()
    midi.close()
    sys.exit()

disp.setup(fullscreen = 0)

## Setup keyboards
keyboards = dict()
_number = 1
for d in devices:
    _keyboard = keyboard.Keyboard(_number, _number-1, inst_mem[mem-1], vol_mem[mem-1], 30, 70, base_mem[mem-1]+ 12*(_number-1), 0)
    keyboards[d] = _keyboard
    _number += 1
for kb in keyboards.values():
    kb.config(midi)
    print "Keyboard", kb, " setup OK!"

## Initialize toggle variables
caps_on = 1
share_sust = 1

## Key-code bindings
getCode = dict()
with open("keybinds.txt") as f:
    for line in f:
        (keyname, code) = line.split()
        getCode[keyname] = int(code)

## Pressed?
for kb in keyboards.values():
    for keyname in getCode.keys():
        kb.pressed[keyname] = 0

## Key-note bindings
getNote = dict()
with open("keyseq.txt") as f:
    for line in f:
        (keyname, note) = line.split()
        getNote[keyname] = int(note)

kbCount = 0
for kb in keyboards.values():
    info = "KB %02d | INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
        (kb.number, kb.inst_num, strNote(kb.baseNote), kb.volume, kb.velocity)
    disp.drawStatus(info, kbCount)
    disp.update()
    kbCount += 1

disp.drawCircle()
disp.drawLogo()
disp.update()

## Main loop
change = 1
while True:
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            ## Identify device
            kb = keyboards[fd]
            # Identify key
            keyname = ecodes.KEY[event.code]
            if event.type == ecodes.EV_KEY and keyname in getCode.keys():
                ## KEYDOWN
                if event.value == 1:
                    # Modifiers
                    if keyname == "KEY_LEFTSHIFT" or keyname == "KEY_RIGHTSHIFT": 
                        change = 10
                    elif keyname == "KEY_CAPSLOCK":
                        caps_on = 1-caps_on
                        if caps_on:
                            # Ungrab keyboard
                            for _fd in devices.keys():
                                try:
                                    devices[_fd].ungrab();
                                    print "Ungrabbed keyboard", devices[_fd].name
                                except IOError:
                                    print "Already ungrabbed."
                            print ""
                        else:
                            # Grab keyboard
                            for _fd in devices.keys():
                                try:
                                    devices[_fd].grab();
                                    print "Grabbed keyboard", devices[_fd].name
                                except IOError:
                                    print "Already grabbed."
                            print ""
                    # Instrument change
                    elif keyname == "KEY_PAGEUP":
                        kb.inst_num = clamp(kb.inst_num+change,0,127)
                        midi.setInstrument(kb.inst_num, kb.channel)
                    elif keyname == "KEY_PAGEDOWN":
                        kb.inst_num = clamp(kb.inst_num-change,0,127)
                        midi.setInstrument(kb.inst_num, kb.channel)
                    # Octave change
                    elif keyname == "KEY_LEFT":
                        kb.baseNote = clamp(kb.baseNote-12,24,72)
                    elif keyname == "KEY_RIGHT":
                        kb.baseNote = clamp(kb.baseNote+12,24,72)
                    # Transpose 
                    elif keyname == "KEY_DOWN":
                        kb.baseNote = clamp(kb.baseNote-1,24,72)
                    elif keyname == "KEY_UP":
                        kb.baseNote = clamp(kb.baseNote+1,24,72)
                    # Volume and velocity change
                    elif keyname == "KEY_HOME":
                        if change == 1:
                            kb.volume = clamp(kb.volume+10,0,127)
                        else:
                            kb.velocity = clamp(kb.velocity+10,0,127)
                    elif keyname == "KEY_END":
                        if change == 1:
                            kb.volume = clamp(kb.volume-10,0,127)
                        else:
                            kb.velocity = clamp(kb.velocity-10,0,127)
                    # Memory events
                    elif keyname in ["KEY_F1","KEY_F2","KEY_F3","KEY_F4","KEY_F5",\
                                    "KEY_F6","KEY_F7","KEY_F8","KEY_F9",\
                                    "KEY_KP1","KEY_KP2","KEY_KP3","KEY_KP4","KEY_KP5",\
                                    "KEY_KP6","KEY_KP7","KEY_KP8","KEY_KP9"]:
                        mem = int(keyname[-1])
                        if change == 10: # Shift down
                            # Save
                            inst_mem[mem-1] = kb.inst_num
                            base_mem[mem-1] = kb.baseNote
                            vol_mem[mem-1] = kb.volume
                            vel_mem[mem-1] = kb.velocity
                            writeMemory(inst_mem, base_mem, vol_mem, vel_mem)
                            print "Save successful!"
                        else:
                            # Load
                            inst_mem = []
                            base_mem = []
                            vol_mem = []
                            vel_mem = []
                            readMemory(inst_mem, base_mem, vol_mem, vel_mem)
                            kb.inst_num = inst_mem[mem-1]
                            kb.baseNote = base_mem[mem-1]
                            kb.volume = vol_mem[mem-1]
                            kb.velocity = vel_mem[mem-1]
                    elif keyname == "KEY_F10" or keyname == "KEY_KP0":
                        # Load system defaults into current mem
                        kb.inst_num = 4
                        kb.baseNote = 36
                        kb.volume = 70
                        kb.velocity = 70
                    # Sustain
                    elif keyname == "KEY_SPACE":
                        if change == 10: # Shift is pressed, toggle sustain-sharing
                            share_sust = 1 - share_sust
                            if share_sust == 1:
                                print "Sharing is caring!"
                                print ""
                            else:
                                print "Individual mode."
                                print ""
                        if share_sust: # Share sustain between instruments
                            for _kb in keyboards.values():
                                _kb.sust = 1
                                for _fd in devices.keys():
                                    for c in devices[_fd].active_keys():
                                        _keyname = ecodes.KEY[c]
                                        if _kb.pressed[_keyname] > 0:
                                            _kb.pressed[_keyname] += 1
                        else: # Individual sustain for instruments
                            kb.sust = 1
                            for c in devices[fd].active_keys():
                                _keyname = ecodes.KEY[c]
                                if kb.pressed[_keyname] > 0:
                                    kb.pressed[_keyname] += 1
                    # Quit
                    elif keyname == "KEY_ESC":
                        for _fd in devices.keys():
                            try:
                                devices[_fd].ungrab();
                            except IOError:
                                print "Already ungrabbed."
                        disp.close()
                        midi.close()
                        disp.pygame.quit()
                        print "Thank you for the music!"
                        print " "
                        sys.exit()
                    # Play note
                    else:
                        kb.noteOf[keyname] = kb.baseNote + getNote.get(keyname, -100)-1 # default -100 as a flag
                        if kb.noteOf[keyname] >= kb.baseNote: # Check flag; ignore if not one of the notes
                            kb.key_down(midi, keyname, kb.noteOf[keyname])


                ## KEY UP
                elif event.value == 0:
                    # Shift up
                    if keyname == "KEY_LEFTSHIFT" or keyname == "KEY_RIGHTSHIFT": 
                        change = 1
                    # Sustain
                    elif keyname == "KEY_SPACE":
                        if share_sust: # Share sustain between instruments
                            for _kb in keyboards.values():
                                _kb.sust = 0
                                for _keyname in _kb.pressed.keys():
                                    if _kb.pressed[_keyname] > 1:
                                        _kb.pressed[_keyname] = 1
                                    elif _kb.pressed[_keyname] == 1:
                                        _kb.pressed[_keyname] = 0
                                        #_note = _kb.baseNote + getNote.get(_keyname, -100)-1
                                        midi.noteOff(_kb.noteOf[_keyname], _kb.channel)
                        else: # Individual sustain for instruments
                            kb.sust = 0
                            for _keyname in kb.pressed.keys():
                                if kb.pressed[_keyname] > 1:
                                    kb.pressed[_keyname] = 1
                                elif kb.pressed[_keyname] == 1:
                                    kb.pressed[_keyname] = 0
                                    _note = kb.baseNote + getNote.get(_keyname, -100)-1
                                    midi.noteOff(_note, kb.channel)
                    # Play note
                    else:
                        #note = kb.baseNote + getNote.get(keyname, -100)-1 # default -100 as a flag
                        if keyname in kb.noteOf.keys(): #kb.noteOf[keyname] >= kb.baseNote: # Check flag; ignore if not one of the notes
                            kb.key_up(midi, keyname, kb.noteOf[keyname])


                ## Update all values
                kb.config(midi)

    disp.fillBackground()
    # Stats
    kbCount = 0
    for kb in keyboards.values():
        if sum(kb.pressed.values()) > 0 or kb.sust > 0:
            disp.pulseCircle()
        info = "KB %02d | INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
            (kb.number, kb.inst_num, strNote(kb.baseNote), kb.volume, kb.velocity)
        disp.drawStatus(info, kbCount)
        kbCount += 1

    # Circle
    disp.drawCircle()
    disp.drawLogo()
    if change == 10: # Draw memory if SHIFT is held
        disp.drawMemory(inst_mem, base_mem, vol_mem, vel_mem)
    disp.update()

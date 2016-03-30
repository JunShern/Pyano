import pygame
import sys
import time
import keyboard
import midi as md
from pygame import gfxdraw
from helpers import *
from memory import *
from evdev import InputDevice, list_devices, categorize, ecodes
from select import select

def drawMemory():
    # Transparent surface
    s = pygame.Surface((width,height))
    s.set_alpha(150)
    s.fill(bg_color)
    screen.blit(s, (0,0))
    # Text colour
    c = pygame.Color(255,255,255)
    # Text
    info = "Default Slot : INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
            (4, strNote(36), 70, 70)
    w, h = pFont.size(info)
    text = pFont.render(info, 1, (255,255,255))
    screen.blit(text, (width/2-w/2, 200))
    for num in range(1,10):
        info = "Memory Slot %i: INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
                (num, inst_mem[num-1], strNote(base_mem[num-1]), vol_mem[num-1], vel_mem[num-1])
        w, h = pFont.size(info)
        text = pFont.render(info, 1, c)
        screen.blit(text, (width/2-w/2, 200 + num*(height-400)/9))

        
pygame.init()
midi = md.Midi()
midi.setup()

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
    pygame.display.quit()
    pygame.quit()
    sys.exit()

## Screen setup
infoObject = pygame.display.Info()
pygame.display.set_caption("Pyano")
img = pygame.image.load("LogoResized.png")
width = int(infoObject.current_w) #img.get_rect().size[0] #
height = int(infoObject.current_h) #img.get_rect().size[1] + 60*num_devices 
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE) #pygame.RESIZABLE
pygame.mouse.set_visible(False) # Hide cursor
print "Screen setup OK!"
## Font setup
pFont = pygame.font.SysFont("monospace", int(width/(width/17)), True)
bigFont = pygame.font.SysFont("monospace", int(width/(width/20)), True)
biggerFont = pygame.font.SysFont("monospace", int(width/(width/30)), True)
biggestFont = pygame.font.SysFont("monospace", int(width/(width/40)), True)
print "Font setup OK!"

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

# Display
#colours_ = [(242,151,84),(221,221,221),(128,206,185)]
colour = (65,170,196) #,(204,50,60),(159,152,126)]
colour_ = colour
circle_w = 8
circle_w_ = 8
circle_r = 230
circle_r_ = 230
bg_color = pygame.Color(5,5,5)
in_color = pygame.Color(15,15,15)
screen.fill(bg_color)
pygame.draw.circle(screen, in_color, (width/2,height/2), circle_r, 0)

rad_step = [1]
walk_count = 1
n = 0

for kb in keyboards.values():
    #pygame.draw.circle(screen, colours[i], (width/2,height/2), circle_r+i*40, circle_w)
    info = "KB %02d | INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
            (kb.number, kb.inst_num, strNote(kb.baseNote), kb.volume, kb.velocity)
    w, h = pFont.size(info)
    text = pFont.render(info, 1, (255,255,255))
    screen.blit(text, (width/2-w/2, (height/2+circle_r) + 20 + n*(h+10) ))
    n += 1

pygame.gfxdraw.filled_circle(screen, width/2, height/2, circle_r, colour)
pygame.gfxdraw.filled_circle(screen, width/2, height/2, circle_r-circle_w, in_color)
pygame.gfxdraw.aacircle(screen, width/2, height/2, circle_r-circle_w, colour)
pygame.gfxdraw.aacircle(screen, width/2, height/2, circle_r, colour)

screen.blit(img, (width/2-img.get_rect().size[0]/2,height/2-img.get_rect().size[1]/2))
pygame.display.update()

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
                        pygame.display.quit()
                        print "Thank you for the music!"
                        print " "
                        midi.close()
                        pygame.quit()
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

    ## Display update
    screen.fill(bg_color)
    pygame.draw.circle(screen, (24,24,24), (width/2,height/2), circle_r_, 0)
    n = 0
    # Stats
    for kb in keyboards.values():
        if sum(kb.pressed.values()) > 0 or kb.sust > 0:
            colour_ = colourWalk(colour_, colour, 80)
            walk_count = 1 - walk_count
            if walk_count == 1:
                circle_r_ = smootherWalk(circle_r_, circle_r-2, circle_r+8, rad_step)
        info = "KB %02d | INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
                (kb.number, kb.inst_num, strNote(kb.baseNote), kb.volume, kb.velocity)
        w, h = pFont.size(info)
        text = pFont.render(info, 1, (255,255,255))
        screen.blit(text, (width/2-w/2, (height/2+circle_r) + 20 + n*(h+10) ))
        n += 1
    # Circle
    pygame.gfxdraw.filled_circle(screen, width/2, height/2, circle_r_, colour_)
    pygame.gfxdraw.filled_circle(screen, width/2, height/2, circle_r_-circle_w_, in_color)
    pygame.gfxdraw.aacircle(screen, width/2, height/2, circle_r_-circle_w_, colour_)
    pygame.gfxdraw.aacircle(screen, width/2, height/2, circle_r_, colour_)

    screen.blit(img, (width/2-img.get_rect().size[0]/2,height/2-img.get_rect().size[1]/2))
    if change == 10: # Draw memory if SHIFT is held
        drawMemory()
    pygame.display.update()
    

import pygame
import pygame.midi
import sys
import time
from helpers import *
from memory import *
from evdev import InputDevice, list_devices, categorize, ecodes
from select import select

class Keyboard(object):
    def __init__(self, number, channel, inst_num, volume, reverb, velocity, baseNote, sust):
        self.number = number
        self.channel = channel
        self.inst_num = inst_num
        self.volume = volume
        self.reverb = reverb
        self.velocity = velocity
        self.baseNote = baseNote
        self.sust = sust
        self.pressed = dict()

    def config(self):
        player.set_instrument(self.inst_num, self.channel) # Instrument
        player.write_short(176+self.channel,7,self.volume) # Volume
        player.write_short(176+self.channel,91,self.reverb) # Reverb

    def key_up(self, keyname):
        if self.pressed[keyname] > 0: # Only turn it OFF if it's ON
            self.pressed[keyname] -= 1
            if self.pressed[keyname] <= 0:
                player.note_off(note, self.velocity, self.channel)

    def key_down(self, keyname):
        self.key_up(keyname) # If it's already ON, turn it OFF first
            
        player.note_on(note, self.velocity, self.channel)
        self.pressed[keyname] += 1
        if self.sust == 1:
            self.pressed[keyname] += 1


pygame.init()

## MIDI init
pygame.midi.init()
print "Choose an output device:"
for i in range(0,pygame.midi.get_count()):
    print "%i : %s" %(i, pygame.midi.get_device_info(i))
dev = int(raw_input(">> " ))
player = pygame.midi.Output(dev)
print "MIDI setup OK!"

## Memory setup
mem = 1
inst_mem = list()
base_mem = list()
vol_mem = list()
vel_mem = list()
readMemory(inst_mem, base_mem, vol_mem, vel_mem)
print "Memory setup OK!"

## Screen setup
infoObject = pygame.display.Info()
width = int(infoObject.current_w * 0.9)
height = int(infoObject.current_h * 0.9)
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
pygame.mouse.set_visible(False) # Hide cursor
print "Screen setup OK!"

## Font setup
pFont = pygame.font.SysFont("monospace", int(width/(width/15)) )
bigFont = pygame.font.SysFont("monospace", int(width/(width/20)) )
biggerFont = pygame.font.SysFont("monospace", int(width/(width/30)) )
biggestFont = pygame.font.SysFont("monospace", int(width/(width/40)) )
print "Font setup OK!"


## Getting devices
devices = list()
for fn in list_devices():
    dev = InputDevice(fn)
    if "eyboard" in dev.name:
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
    player.abort()
    player.close()
    pygame.quit()
    sys.exit()


## Setup keyboards
keyboards = dict()
_number = 1
for d in devices:
    _keyboard = Keyboard(_number, _number-1, inst_mem[mem-1], vol_mem[mem-1], 30, 70, base_mem[mem-1]+ 12*(_number-1), 0)
    keyboards[d] = _keyboard
    _number += 1
for kb in keyboards.values():
    kb.config()
    print "Keyboard", kb, " setup OK!"

## Initialize caps
caps_on = 1

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
bg_color = pygame.Color(47-10,52-10,58-10)
screen.fill(bg_color)

i = 2
for kb in keyboards.values():
    info = "KB %02d | INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
            (kb.number, kb.inst_num, kb.baseNote, kb.volume, kb.velocity)
    w, h = bigFont.size(info)
    text = bigFont.render(info, 1, (255,255,255))
    screen.blit(text, (width/2-w/2, height*i/4-h-h))
    i += 1

hit_ctrl = "Hit CAPS LOCK for help!"
w, h = bigFont.size(hit_ctrl)
text = bigFont.render(hit_ctrl, 1, (200,200,255))
screen.blit(text, (width/2-w/2, h))
pygame.display.update()

## Main loop
while True:

    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            # Identify device
            kb = keyboards[fd]
            if event.type == ecodes.EV_KEY and event.value != 2:
                # Identify key and note
                keyname = ecodes.KEY[event.code]
                note = kb.baseNote + getNote.get(keyname, -100)-1 # default -100 as a flag
                keydown = event.value
                #print keyname, note

                # Modifiers
                change = 1
                if getCode["KEY_LEFTSHIFT"] in devices[fd].active_keys(): # Left shift
                    change = 10
                if keyname == "KEY_CAPSLOCK":
                    if keydown == True:
                        caps_on = 1-caps_on
                        if caps_on:
                            print "Sharing is caring!"
                        else:
                            print "Individual mode."

                ## Play note
                if note >= kb.baseNote: # Check flag; ignore if not one of the notes
                    if keydown == True:
                        kb.key_down(keyname)
                    elif keydown == False:
                        kb.key_up(keyname)

                ## Instrument change
                elif keyname == "KEY_PAGEUP":
                    if keydown == True:
                        kb.inst_num = clamp(kb.inst_num+change,0,127)
                        player.set_instrument(kb.inst_num, kb.channel)
                elif keyname == "KEY_PAGEDOWN":
                    if keydown == True:
                        kb.inst_num = clamp(kb.inst_num-change,0,127)
                        player.set_instrument(kb.inst_num, kb.channel)

                ## Octave change
                elif keyname == "KEY_LEFT":
                    if keydown == True:
                        kb.baseNote = clamp(kb.baseNote-12,24,60)
                elif keyname == "KEY_RIGHT":
                    if keydown == True:
                        kb.baseNote = clamp(kb.baseNote+12,24,60)
                ## Transpose 
                elif keyname == "KEY_DOWN":
                    if keydown == True:
                        kb.baseNote = clamp(kb.baseNote-1,24,60)
                elif keyname == "KEY_UP":
                    if keydown == True:
                        kb.baseNote = clamp(kb.baseNote+1,24,60)

                ## Volume and velocity change
                elif keyname == "KEY_HOME":
                    if keydown == True:
                        if change == 1:
                            kb.volume = clamp(kb.volume+10,0,127)
                        else:
                            kb.velocity = clamp(kb.velocity+10,0,127)
                elif keyname == "KEY_END":
                    if keydown == True:
                        if change == 1:
                            kb.volume = clamp(kb.volume-10,0,127)
                        else:
                            kb.velocity = clamp(kb.velocity-10,0,127)

                ## Sustain
                elif keyname == "KEY_SPACE":
                    if caps_on:
                        ## Share sustain between instruments
                        for _kb in keyboards.values():
                            if keydown == True:
                                _kb.sust = 1
                                player.write_short(176+_kb.channel,64,127)
                                for _fd in devices.keys():
                                    for c in devices[_fd].active_keys():
                                        _keyname = ecodes.KEY[c]
                                        if _kb.pressed[_keyname]:
                                            _kb.pressed[_keyname] += 1
                            elif keydown == False:
                                _kb.sust = 0
                                player.write_short(176+_kb.channel,64,0)
                                for _keyname in _kb.pressed.keys():
                                    if _kb.pressed[_keyname] > 0:
                                        _kb.pressed[_keyname] -= 1
                                    if _kb.pressed[_keyname] <= 0:
                                        _note = _kb.baseNote + getNote.get(_keyname, -100)-1
                                        player.note_off(_note, 127, _kb.channel)
                    else:
                        ## Individual sustain for instruments
                        if keydown == True:
                            kb.sust = 1
                            player.write_short(176+kb.channel,64,127)
                            for c in devices[fd].active_keys():
                                _keyname = ecodes.KEY[c]
                                if kb.pressed[_keyname]:
                                    kb.pressed[_keyname] += 1
                        elif keydown == False:
                            kb.sust = 0
                            player.write_short(176+kb.channel,64,0)
                            for _keyname in kb.pressed.keys():
                                if kb.pressed[_keyname] > 0:
                                    kb.pressed[_keyname] -= 1
                                if kb.pressed[_keyname] <= 0:
                                    _note = kb.baseNote + getNote.get(_keyname, -100)-1
                                    player.note_off(_note, 127, kb.channel)

                ## Quit
                if keyname == "KEY_ESC":
                    pygame.display.quit()
                    print "Thank you for the music!"
                    player.abort()
                    player.close()
                    pygame.quit()
                    sys.exit()

                ## Update all values
                kb.config()

    ## Display update
    screen.fill(bg_color)
    i = 2
    for kb in keyboards.values():
        info = "KB %02d | INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
            (kb.number, kb.inst_num, kb.baseNote, kb.volume, kb.velocity)
        w, h = bigFont.size(info)
        text = bigFont.render(info, 1, (255,255,255))
        screen.blit(text, (width/2-w/2, height*i/4-h-h))
        i += 1
    pygame.display.update()
    
"""
    info = "INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
            (inst_num, baseNote, volume, velocity)
    w, h = bigFont.size(info)
    text = bigFont.render(info, 1, (255,255,255))
    screen.blit(text, (width/2-w/2, height-h-h))
"""
"""
                ## Memory events
                if mods & pygame.KMOD_CTRL:
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3,
                                        pygame.K_4, pygame.K_5, pygame.K_6,
                                        pygame.K_7, pygame.K_8, pygame.K_9]:
                            mem = int(key[0])
                            if change == 10:
                                # Save
                                inst_mem[mem-1] = inst_num
                                base_mem[mem-1] = baseNote
                                vol_mem[mem-1] = volume
                                vel_mem[mem-1] = velocity
                                writeMemory(inst_mem, base_mem, vol_mem, vel_mem)
                            else:
                                # Load
                                inst_mem = []
                                base_mem = []
                                vol_mem = []
                                vel_mem = []
                                readMemory(inst_mem, base_mem, vol_mem, vel_mem)
                                inst_num = inst_mem[mem-1]
                                player.set_instrument(inst_num,channel)
                                baseNote = base_mem[mem-1]
                                volume = vol_mem[mem-1]
                                player.write_short(176+channel,7,volume)
                                velocity = vel_mem[mem-1]
                        elif event.key == pygame.K_0:
                            # Load system defaults into current mem
                            inst_num = 4
                            player.set_instrument(inst_num,channel)
                            baseNote = 36
                            volume = 50
                            player.write_short(176+channel,7,volume)
                            velocity = 70
"""
"""



"""
"""
    # Draw
    drawKeyboard(x,y)
    if mods & pygame.KMOD_CAPS:
        drawControls()
    if mods & pygame.KMOD_CTRL:
        drawMemory()
    else:
        hit_ctrl = "Hit CAPS LOCK for help!"
        w, h = bigFont.size(hit_ctrl)
        text = bigFont.render(hit_ctrl, 1, (200,200,255))
        screen.blit(text, (width/2-w/2, h))

    info = "INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
            (inst_num, baseNote, volume, velocity)
    w, h = bigFont.size(info)
    text = bigFont.render(info, 1, (255,255,255))
    screen.blit(text, (width/2-w/2, height-h-h))
"""

"""
    event = pygame.event.wait()
    screen.fill(bg_color)

    # Screen resize
    if event.type == pygame.VIDEORESIZE:
        width = event.w
        height = event.h
        screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        x = width/15
        y = height/3.5
        # Font resize
        pFont = pygame.font.SysFont("monospace", int(width/(1366/15)) )
        bigFont = pygame.font.SysFont("monospace", int(width/(1366/20)) )
        biggerFont = pygame.font.SysFont("monospace", int(width/(1366/30)) )
        biggestFont = pygame.font.SysFont("monospace", int(width/(1366/40)) )
        
"""
"""
## Draw keyboards
# Key layout
downkeys = []
rows = ["1234567890-=","qwertyuiop[]\\","asdfghjkl;'","zxcvbnm,./"]
keys = list(rows[0]) + list(rows[1]) + list(rows[2]) + list(rows[3])
pressedStates = [0 for k in keys]
pressed = dict(zip(keys, pressedStates))
# Key mapping
order = list("zsxdcvgbhnjmq2w3er5t6y7ui9o0p[=]+\\")
mapping = dict()
count = 0
for letter in seq:
    mapping[letter] =  count
    count += 1
print "Keys setup OK!"
"""
"""
# Opening credits
for a in range(1,150):
    screen.fill(bg_color)
    # Title
    openColor = colorClamp(bg_color.r+a,bg_color.g+a,bg_color.b+a)
    w, h = biggestFont.size("Pyano.")
    titleText = biggestFont.render("Pyano ", 1, openColor)
    screen.blit(titleText, (width/2,height/2))
    # Credits
    openColor = colorClamp(openColor.r-20,openColor.g-20,openColor.b-20)
    titleText = biggestFont.render("Pyano ", 1, openColor)
    w_, h_ = bigFont.size("version 1.0 | 2015")
    creditText = bigFont.render("version 1.0 | 2015", 1, openColor)
    screen.blit(creditText, (width/2+w,height/2+h_*2/3))
    pygame.display.update()
    time.sleep(0.005)
event = pygame.event.wait()
time.sleep(1)
# Wait for keypress
#while event.type not in (pygame.KEYDOWN, pygame.KEYUP):
#    event = pygame.event.wait()

# Keyboard opening animation
x = width/15
y = height/3.5
for i in range(-50,10):
    screen.fill(bg_color)
    pygame.display.update()
    time.sleep(0.001)
"""

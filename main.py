import pygame
import pygame.midi
import sys
import time

def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

def colorClamp(r, g, b):
    return pygame.Color(clamp(r,0,255),
                        clamp(g,0,255),
                        clamp(b,0,255))

def readMemory():
    with open("memory.txt") as f:
        lines = [line.strip() for line in f]
    for num in lines[0].split(' '):
        inst_mem.append(int(num))
    for num in lines[1].split(' '):
        base_mem.append(int(num))
    for num in lines[2].split(' '):
        vol_mem.append(int(num))
    for num in lines[3].split(' '):
        vel_mem.append(int(num))

def writeMemory(num):
    with open("memory.txt", 'w') as f:
        for i in inst_mem:
            f.write("%i " %i)
        f.write("\n")
        for b in base_mem:
            f.write("%i " %b)
        f.write("\n")
        for v in vol_mem:
            f.write("%i " %v)
        f.write("\n")
        for s in vel_mem:
            f.write("%i " %s)
        f.write("\n")

def drawMemory():
    # Transparent surface
    s = pygame.Surface((width,height))
    s.set_alpha(220)
    s.fill(bg_color)
    screen.blit(s, (0,0))
    # Text colour
    c = pygame.Color(255,255,255)
    if change == 10:
        c = pygame.Color(160,255,255)
    # Text
    info = "Memory Slot 0: INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
            (4, 36, 50, 70)
    w, h = bigFont.size(info)
    text = bigFont.render(info, 1, (255,255,255))
    screen.blit(text, (width/2-w/2, 200))
    for num in range(1,10):
        info = "Memory Slot %i: INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
                (num, inst_mem[num-1], base_mem[num-1], vol_mem[num-1], vel_mem[num-1])
        w, h = bigFont.size(info)
        text = bigFont.render(info, 1, c)
        screen.blit(text, (width/2-w/2, 200 + num*(height-400)/9))

def controlsText(key_txt, info_txt, xpos, yCount, color_l, color_r):
    w, h = bigFont.size(key_txt)
    text = bigFont.render(key_txt, 1, color_l)
    screen.blit(text, (xpos-w-20, 20+h*yCount))
    text = bigFont.render(info_txt, 1, color_r)
    screen.blit(text, (xpos+20, 20+h*yCount))

def drawControls():
    # Transparent surface
    s = pygame.Surface((width,height))
    s.set_alpha(230)
    s.fill(bg_color)
    screen.blit(s, (0,0))

    color_l = pygame.Color(95,200,226)
    color_r = pygame.Color(255,255,255)
    xpos = width/3
    yCountPadding = 7
    # CONTROLS
    controls_str = "C O N T R O L S"
    w, h = biggerFont.size(controls_str)
    controls_txt = biggerFont.render(controls_str, 1, color_r)
    screen.blit(controls_txt, (xpos-w-20, 120))
    # VOLUME
    controlsText("HOME", "Volume +10", xpos, yCountPadding+1, color_l, color_r)
    controlsText("END", "Volume -10", xpos, yCountPadding+2, color_l, color_r)
    controlsText("SHIFT + HOME", "Velocity +10", xpos, yCountPadding+3, color_l, color_r)
    controlsText("SHIFT + END", "Velocity -10", xpos, yCountPadding+4, color_l, color_r)
    # INSTRUMENT
    controlsText("PAGE UP", "Change instrument +1", xpos, yCountPadding+6, color_l, color_r)
    controlsText("PAGE DOWN", "Change instrument -1", xpos, yCountPadding+7, color_l, color_r)
    controlsText("SHIFT + PAGE UP", "Change instrument +10", xpos, yCountPadding+8, color_l, color_r)
    controlsText("SHIFT + PAGE DOWN", "Change instrument -10", xpos, yCountPadding+9, color_l, color_r)
    # TRANSPOSE
    controlsText("UP ARROW", "Transpose +1 semitone", xpos, yCountPadding+11, color_l, color_r)
    controlsText("DOWN ARROW", "Transpose -1 semitone", xpos, yCountPadding+12, color_l, color_r)
    controlsText("RIGHT ARROW", "Transpose +1 octave", xpos, yCountPadding+13, color_l, color_r)
    controlsText("LEFT ARROW", "Transpose -1 octave", xpos, yCountPadding+14, color_l, color_r)
    # MEMORY 
    controlsText("CTRL + [1:9]", "Load instrument, volume and transposition data from saved memory bank", xpos, yCountPadding+16, color_l, color_r)
    controlsText("CTRL + SHIFT + [1:9]", "Save current instrument, volume and transposition data to memory bank", xpos, yCountPadding+17, color_l, color_r)
    # SUSTAIN
    controlsText("SPACE", "Hold/release sustain", xpos, yCountPadding+19, color_l, color_r)


def drawKey(key, pos):
    "Draw a single keyboard key; pos is the top left corner"
    w = ((width*4/5)/16) * 4/5
    points = [(pos[0],pos[1]),(pos[0]+w*3/4,pos[1]),(pos[0]+w,pos[1]+w/4),
            (pos[0]+w,pos[1]+w*8/7),(pos[0],pos[1]+w*8/7)]
    points_ = []
    points_edge = []

    # Sharps
    if mapping.get(key,-1) in [1,3,6,8,10,13,15,18,20,22,25,27,30]:
        color = pygame.Color(242,151,84)
        color_ = pygame.Color(204,50,70)
    # Naturals
    elif mapping.get(key,-1) > -1:
        color = pygame.Color(128,206,185)
        color_ = pygame.Color(65,170,196)
    # Empty
    else:
        color = pygame.Color(221,221,221)
        color_ = pygame.Color(159,152,126)


    if pressed[key] > 0:
        color = pygame.Color(125,223,87)
        color_ = pygame.Color(33,131,68)
        for p in points:
            points_.append((p[0]-4, p[1]-4))
            points_edge.append((p[0]-1,p[1]-1))
    else:
        for p in points:
            points_.append((p[0]-6, p[1]-8))
            points_edge.append((p[0]-3,p[1]-5))

    # Shadow
    pygame.draw.polygon(screen, colorClamp(bg_color.r-20,bg_color.g-20,bg_color.b-20), points, 0)
    pygame.draw.aalines(screen, colorClamp(bg_color.r-20,bg_color.g-20,bg_color.b-20), True, points, 1)
    # Key Edge
    pygame.draw.polygon(screen, color_, points_edge, 0)
    pygame.draw.aalines(screen, color_, True, points_edge, 1)
    # Key
    pygame.draw.polygon(screen, color, points_, 0)
    pygame.draw.aalines(screen, color, True, points_, 1)

    # Text
    note = baseNote + mapping.get(key, -100) # default -100 as a flag
    if note >= baseNote:
        text = pFont.render(str(note), 1, colorClamp(color.r-80,color.g-80,color.b-80))
        screen.blit(text, (points_[0][0]+5,points_[0][1]+5))

    return 

def drawKeyboard(x, y):
    w = (width*4/5)/13
    for j in range(1,5):
        row = list(rows[j-1])
        i = 0
        for key in row:
            drawKey(key, (x+w/2*j+i*w, y+(j-1)*w) )
            i += 1
    return

def key_up(key):
    if pressed[key] > 0: # Only turn it OFF if it's ON
        pressed[key] -= 1
        if pressed[key] <= 0:
            player.note_off(note, velocity, channel)

def key_down(key):
    key_up(key) # If it's already ON, turn it OFF first
        
    player.note_on(note, velocity, channel)
    pressed[key] += 1
    if sust == 1:
        pressed[key] += 1


pygame.init()


## Memory setup
mem = 1
inst_mem = list()
base_mem = list()
vol_mem = list()
vel_mem = list()
readMemory()
print "Memory setup OK!"


## MIDI setup
pygame.midi.init()
print "Choose an output device:"
for i in range(0,pygame.midi.get_count()):
    print "%i : %s" %(i, pygame.midi.get_device_info(i))
dev = int(raw_input(">> " ))
player = pygame.midi.Output(dev)
inst_num = inst_mem[mem-1]
channel = 0
player.set_instrument(inst_num,channel)
volume = vol_mem[mem-1]
player.write_short(176+channel,7,volume)
reverb = 30
player.write_short(176+channel,91,reverb) 
velocity = 70
print "MIDI setup OK!"

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

## Draw keyboards
# Key layout
downkeys = []
sust = 0
rows = ["1234567890-=","qwertyuiop[]\\","asdfghjkl;'","zxcvbnm,./"]
keys = list(rows[0]) + list(rows[1]) + list(rows[2]) + list(rows[3])
pressedStates = [0 for k in keys]
pressed = dict(zip(keys, pressedStates))
# Key mapping
seq = list("zsxdcvgbhnjmq2w3er5t6y7ui9o0p[=]+\\")
mapping = dict()
count = 0
for letter in seq:
    mapping[letter] =  count
    count += 1
baseNote = base_mem[mem-1]

print "Keys setup OK!"

# Colour scheme
bg_color = pygame.Color(47-10,52-10,58-10)

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
    drawKeyboard(x,y*i/10)
    pygame.display.update()
    time.sleep(0.001)

screen.fill(bg_color)
drawKeyboard(x, y)
info = "INST %03d | BASE %03d | VOL %03d | VEL %03d" %\
        (inst_num, baseNote, volume, velocity)
w, h = bigFont.size(info)
text = bigFont.render(info, 1, (255,255,255))
screen.blit(text, (width/2-w/2, height-h-h))
hit_ctrl = "Hit CAPS LOCK for help!"
w, h = bigFont.size(hit_ctrl)
text = bigFont.render(hit_ctrl, 1, (200,200,255))
screen.blit(text, (width/2-w/2, h))
pygame.display.update()

## Main loop
while 1:
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

    # Modifiers
    change = 1
    mods = pygame.key.get_mods()
    if mods & pygame.KMOD_SHIFT:
        change = 10

    # Keypresses
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        key = pygame.key.name(event.key)
        note = baseNote + mapping.get(key, -100) # default -100 as a flag

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
                        writeMemory(mem)
                    else:
                        # Load
                        inst_mem = []
                        base_mem = []
                        vol_mem = []
                        vel_mem = []
                        readMemory()
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

        ## Play note
        elif note >= baseNote: # Check flag; ignore if not one of the notes
            if event.type == pygame.KEYDOWN :
                key_down(key)
            elif event.type == pygame.KEYUP :
                key_up(key)

        ## Instrument change
        elif event.key == pygame.K_PAGEUP:
            if event.type == pygame.KEYDOWN:
                inst_num = clamp(inst_num+change,0,127)
                player.set_instrument(inst_num, channel)
        elif event.key == pygame.K_PAGEDOWN:
            if event.type == pygame.KEYDOWN:
                inst_num = clamp(inst_num-change,0,127)
                player.set_instrument(inst_num, channel)

        ## Volume and velocity change
        elif event.key == pygame.K_HOME:
            if event.type == pygame.KEYDOWN:
                if change == 1:
                    volume = clamp(volume+10,0,127)
                    player.write_short(176+channel,7,volume)
                else:
                    velocity = clamp(velocity+10,0,127)
#                y = height/3*(127-volume)/127 # Move keyboard height
        elif event.key == pygame.K_END:
            if event.type == pygame.KEYDOWN:
                if change == 1:
                    volume = clamp(volume-10,0,127)
                    player.write_short(176+channel,7,volume)
                else:
                    velocity = clamp(velocity-10,0,127)
#                y = height/3*(127-volume)/127 # Move keyboard height

        ## Octave change
        elif event.key == pygame.K_LEFT:
            if event.type == pygame.KEYDOWN:
                baseNote = clamp(baseNote-12,24,60)
        elif event.key == pygame.K_RIGHT:
            if event.type == pygame.KEYDOWN:
                baseNote = clamp(baseNote+12,24,60)
        ## Transpose 
        elif event.key == pygame.K_DOWN:
            if event.type == pygame.KEYDOWN:
                baseNote = clamp(baseNote-1,24,60)
        elif event.key == pygame.K_UP:
            if event.type == pygame.KEYDOWN:
                baseNote = clamp(baseNote+1,24,60)

        ## Sustain
        elif event.key == pygame.K_SPACE:
            if event.type == pygame.KEYDOWN:
                sust = 1
                player.write_short(176+channel,64,127)
                for k in keys:
                    if pressed[k]:
                        pressed[k] += 1
            elif event.type == pygame.KEYUP:
                sust = 0
                player.write_short(176+channel,64,0)
                for k in keys:
                    if pressed[k] > 0:
                        pressed[k] -= 1
                    if pressed[k] <= 0:
                        note = baseNote + mapping.get(k, -100) 
                        player.note_off(note, 127, channel)
            player.set_instrument(inst_num, channel) # Inst changes to gunshot after SPACE. Why?


        ## Quit
        if event.key == pygame.K_ESCAPE:
            pygame.display.quit()
            player.abort()
            player.close()
            pygame.quit()
            print "Thank you for the music!"
            sys.exit()

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

    pygame.display.update()


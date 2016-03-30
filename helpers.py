import pygame
import random

def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

def colorClamp(r, g, b):
    return pygame.Color(clamp(r,0,255),
                        clamp(g,0,255),
                        clamp(b,0,255))

def smootherWalk(val, low, high, rad_step):
    if val+rad_step[0] >= high:
        rad_step[0] = -rad_step[0]
        return val+rad_step[0]
    elif val+rad_step[0] <= low:
        rad_step[0] = -rad_step[0]
        return val+rad_step[0]
    else:
        return val+rad_step[0]
#        if random.random()>0.5:
#            return val+rad_step[0]
#        else:
#            return val-rad_step[0]

def randomWalk(val, low, high, step):
    if val+step > high:
        return val-step
    elif val-step < low:
        return val+step
    else:
        if random.random()>0.5:
            return val+step
        else:
            return val-step

def colourWalk(colour, ori, bound):
    step = 5
    r = randomWalk(colour[0], ori[0]-bound, ori[0]+bound, step)
    g = randomWalk(colour[1], ori[1]-bound, ori[1]+bound, step)
    b = randomWalk(colour[2], ori[2]-bound, ori[2]+bound, step)
    return colorClamp(r,g,b)

def strNote(noteNum):
    octave = int(noteNum/12) - 1;
    notes = "C C# D D# E F F# G G# A A# B"
    notes = notes.split(' ')
    n = noteNum % 12
    octave = noteNum/12
    name = "%s%d" %(notes[n], octave)
    return name

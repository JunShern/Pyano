import pygame

def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

def colorClamp(r, g, b):
    return pygame.Color(clamp(r,0,255),
                        clamp(g,0,255),
                        clamp(b,0,255))


import pygame.midi

class Midi(object):
    def __init__(self):
        self.player = None

    def setup(self):
        ## MIDI init
        pygame.midi.init()
        print "Choose an output device:"
        for i in range(0,pygame.midi.get_count()):
            print "%i : %s" %(i, pygame.midi.get_device_info(i))
        dev = int(raw_input(">> " ))
        self.player = pygame.midi.Output(dev)
        print "MIDI setup OK!"

    def close(self):
        self.player.abort()
        self.player.close()

    def setInstrument(self, inst_num, channel):
        self.player.set_instrument(inst_num, channel)

    def noteOff(self, note, channel):
        self.player.note_off(note, 127, channel)

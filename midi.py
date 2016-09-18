import pygame.midi

class Midi(object):
    def __init__(self):
        self.player = None

    def setup(self):
        ## MIDI init
        pygame.midi.init()
        ## Wait for FluidSynth to be ready
        synthReady = False
        while (synthReady == False):
            for i in range(0,pygame.midi.get_count()):
                # print "Trying %i: %s" %(i, pygame.midi.get_device_info(i))
                # get_device_info(i) returns a list of info, [1] gives the device namestring
                if ("Synth" in pygame.midi.get_device_info(i)[1]) : 
                    self.player = pygame.midi.Output(i)
                    print "Using %s" %(pygame.midi.get_device_info(i)[1])
                    synthReady = True
        print "MIDI setup OK!"

    def close(self):
        #self.player.abort()
        self.player.close()

    def setInstrument(self, inst_num, channel):
        self.player.set_instrument(inst_num, channel)

    def noteOff(self, note, channel):
        self.player.note_off(note, 127, channel)

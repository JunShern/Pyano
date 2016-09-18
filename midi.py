import pygame.midi

class Midi(object):
    def __init__(self):
        self.player = None

    def setup(self):
        ## MIDI init
        pygame.midi.init()
        ## Wait for FluidSynth to be ready
        synthReady = False
        while (not synthReady):
            # Automatically look for a "Synth" output
            print "Checking for \'Synth\' in available MIDI outputs:"
            for i in range(0,pygame.midi.get_count()):
                # get_device_info(i) returns a list of info, [1] gives the device namestring
                print "%i: %s" %(i, pygame.midi.get_device_info(i)[1])
                if ("Synth" in pygame.midi.get_device_info(i)[1]) : 
                    self.player = pygame.midi.Output(i)
                    synthReady = True
            # If no "Synth" output, prompt user for choice
            if (not synthReady):
                selection = int(raw_input("None found. Please select an output >> "))
                if selection in range(0,pygame.midi.get_count()):
                    synthReady = True
                else: 
                    print "Invalid output choice, please select an output between 0 and %i" %(pygame.midi.get_count())
        
        print "MIDI setup OK! Using %s" %(pygame.midi.get_device_info(i)[1])

    def close(self):
        #self.player.abort()
        self.player.close()

    def setInstrument(self, inst_num, channel):
        self.player.set_instrument(inst_num, channel)

    def noteOff(self, note, channel):
        self.player.note_off(note, 127, channel)

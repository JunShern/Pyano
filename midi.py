import pygame.midi
import mido

class Midi(object):
    def __init__(self):
        self.outport = None
        with mido.open_output('pyano_out', virtual=True, autoreset=True) as outport:
            self.outport = outport

    def close(self):
        print "Close"

    def setInstrument(self, inst_num, channel):
        msg = mido.Message('program_change', channel=channel, program=inst_num)
        print msg
        self.outport.send(msg)

    def setVolume(self, volume, channel):
        msg = mido.Message('control_change', channel=channel, control=7, value=volume) # Control=7 for volume
        print msg
        self.outport.send(msg)

    def noteOn(self, note, velocity, channel):
        msg = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
        print msg
        self.outport.send(msg)

    def noteOff(self, note, channel):
        msg = mido.Message('note_off', note=note, velocity=127, channel=channel)
        print msg
        self.outport.send(msg)

##About

Pyano is a free and open-source virtual MIDI controller program which allows you to use your keyboard (as in QWERTY keyboard) as a keyboard instrument (as in pianos, harpsichords, organs).

Born of a need for an instrument to play while away from home, the Pyano project hopes to allow musicians to express themselves with nothing more than a computer or laptop, and optionally many external USB keyboards.

Watch the demo [here](https://www.youtube.com/watch?v=W8SxEO2BcnQ)!

##How It Works

Pyano focuses on the front-end of things; which is to say, it provides a user interface that captures keystroke events from the user's keyboard. Upon detecting a keypress, the program sends a MIDI signal to an external synthesizer program (such as Fluidsynth), which produces the sounds. On its own, Pyano does **not** make any sound.

##Getting Started

###Prerequisites (Linux)

1. The latest version of Pyano can only be run on Linux, and has been tested on Ubuntu 14.04 and 16.04, though other flavours of Linux should work. Clone the latest build of Pyano from the Github [page](https://github.com/JunShern/Pyano) using:
   ```
   git clone https://github.com/JunShern/Pyano.git
   ```
   Alternatively, there is an older version on branch `version1` which has fewer features and only supports one instrument at a time, that should work on other operating systems (tested on Windows 8 and Windows 10, but there will likely be latency issues depending on your setup).

2. Pyano is built on [Python 2.7](https://www.python.org/) (already included on most Linux OSes - just run `python` in a terminal to make sure that the version is 2.7.*), the [Pygame library](http://www.pygame.org/hifi.html) and the [Python EvDev](https://python-evdev.readthedocs.org/en/latest/) library, so you need to have these installed on your computer:
   ```bash
   # Install Pygame
   sudo apt-get install python-pygame

   # Install EvDev using pip
   sudo apt-get install python-dev python-pip gcc
   sudo apt-get install linux-headers-$(uname -r)
   sudo pip install evdev
   ```

3. You also need to install a real-time software synthesizer which supports MIDI input. ([Fluidsynth](http://www.fluidsynth.org/) has been tested and is recommended)
   ```bash
   sudo apt-get install fluidsynth
   ```

4. Software synths like FluidSynth require SoundFonts to produce sound; these SoundFonts tell your synthesizer what sounds to make when Pyano asks the synthesizer to 'Play middle C on a trombone'.
   Many different SoundFonts exist, but the 'FluidR3_GM' SoundFont has been tested and sounds great. Recent versions of Ubuntu come with this SoundFont (located at `/usr/share/sounds/sf2/FluidR3_GM.sf2`, but you can easily find and download other SoundFonts online.

###Prerequisites (macOS)

1. macOS support is currently under development and unstable. Clone the latest build of Pyano from the Github [page](https://github.com/JunShern/Pyano) using:
   ```
   git clone https://github.com/JunShern/Pyano.git
   ```
Branch off of `mac-port` and PR changes against it.

2. Install [Homebrew](http://brew.sh/index.html) if you haven't already.

3. Ensure you have Python 2.7.* installed by running `python --version` in Terminal. Install the [Pygame library](http://www.pygame.org/hifi.html) by running `brew install pygame`. EvDev is not supported on macOS and alternative options are currently being investigated.

4. You also need to install a real-time software synthesizer which supports MIDI input. ([Fluidsynth](http://www.fluidsynth.org/) has been tested and is recommended)
   ```bash
   brew install fluid-synth
   ```
5. Software synths like FluidSynth require SoundFonts to produce sound; these SoundFonts tell your synthesizer what sounds to make when Pyano asks the synthesizer to 'Play middle C on a trombone'. Many different SoundFonts exist, but the 'FluidR3_GM' SoundFont has been tested and sounds great. MacOS machines do not come with 'FluidR3_GM' but the .sf2 file itself is readily available online. Place the downloaded file into the `soundfonts` folder.

###Setup
There are many ways to fit Pyano into your musical workflow, but it all involves connecting Pyano to a software synth. The simplest, officially supported setup is described below:

####Using FluidSynth with ALSA
1. Open up a terminal, and navigate to where you cloned the Pyano repository. For example,
   ```bash
   cd /home/junshern/Pyano
   ```

2. Use the script 'playpyano.sh' to automatically run FluidSynth and Pyano for you.
   ```bashbash
   ./playpyano start
   ```
   The script assumes you have FluidSynth and ALSA installed, and your soundfont is located at `/usr/share/sounds/sf2/FluidR3_GM.sf2`. You can change the path to point to any .sf2 soundfont you like.

3. Make some music! (Look below for Instructions on how to play)

4. After you're done, run
   ```bash
   ./playpyano stop
   ```
   to close FluidSynth. This is less useful for this simple setup of using FluidSynth with ALSA, but if you have a complicated setup such as using JACK to route your audio into various places, you can tailor the script to your needs (see the 'makemusic' script for a more complicated workflow using JACK and SooperLooper for live looping).


##Screenshots

Current version, shows multiple keyboards and status lines for each keyboard:

![multikey](https://raw.githubusercontent.com/JunShern/Pyano/master/img/multikey.png?raw=true "multikey")

Older, Windows-compatible version (in branch version1):

![version1](https://raw.githubusercontent.com/JunShern/Pyano/master/img/version1.png?raw=true "version1")


##Instructions

* **Volume** control UP/DOWN using HOME/END buttons
  * Note that HOME/END only controls volume for your current keyboard; if you'd like to change global volume, use your mouse to manually change the volume settings on your system tray

* **Velocity** control UP/DOWN using SHIFT+HOME/END

* Use the SPACEBAR as a **sustain** pedal
  * SHIFT+SPACE toggles sharing of sustain between multiple keyboards.

* **Transpose** your instrument using the arrow keys
  * Use the UP/DOWN arrow keys to shift all active keyboards (except percussion) by one semitone.
  * Use SHIFT+UP (or DOWN) to shift only your current instrument by one semitone.
  >(Pro tip: Hit it twice for that chorus, nobody likes a one-semitone key change)

  * Want to go higher but reached the top of your keyboard? Just hit the RIGHT (or LEFT) arrow key to shift your instrument by an octave.

* **Change instruments** using PAGEUP and PAGEDOWN
  * The instrument sound you get will depend on your software synthesizer and the SoundFont you have chosen. For example, FluidGM2.SF has over 100 instruments and sounds you can use.
  * Percussion instruments are a special case; see point "Percussion instruments" below.

* **Save up to 9 settings** in the program's sound bank
  * Use CTRL+SHIFT+F# or CTRL+SHIFT+KP# where # is the sound bank number you want to save it to.

* Quickly **load up saved settings** to jump between your favourite instruments
  * Just hit F# or KP# where # is the sound bank number you want to load from.

* Access **percussion instruments** using F10 or KP0
  * Jump back to non-percussion instruments using any other F# or KP# keys.

* Use multiple keyboards for **multiple instruments**!
  * Plug in an extra USB keyboard before you run Pyano; you'll be able to control each keyboard individually as a different instrument. Handy for getting more octaves in range!
  * Be careful though, Pyano doesn't support plugging/unplugging while running, so don't unplug your keyboards after Pyano has started up.

##Similar projects

* [Virtual MIDI Piano Keyboard (VMPK)](http://vmpk.sourceforge.net/)

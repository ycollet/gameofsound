A game of life with produces sound.

The LIF files come from http://plife.sourceforge.net/

This program uses matplotlib, numpy and scipy.
ffmpeg is used during rendering (optional, only if --mov-file is passed on the command line).

Example of use:

    $ python3 gameoflife.py --custom data/RPENTO.LIF --exportsound --fmin=25 --fmax=7000 --soundtime=0.1 --grid-size=100 --soundenv=10

Once you are satisfied by the evolution, you can close the matplotlib window. The wav file will be generated after the matplotlib is closed.

Options:

    --grid-size=size - the grid size of the game of life: [0 -> N:0 -> N]
    --mov-file - export a mov file of the evolution of the game
    --interval - time in ms between two frames
    --mov-time - duration to save (in s)
    --glider - add a glider in the grid
    --gosper - add a gosper in the grid
    --rectangle=size  - add a square of size [size:size] in the grid
    --line=size - add a line of length size in the grid
    --custom=filename - use <filename> LIF file to file the grid
    --exportsound - export a wav file
    --soundfilename=filename - file name of the wav file
    --fmin=value - minimum rendered frequency
    --fmax=value - maximum rendered frequency
    --soundtime=value - one step of the evolution is rendered during <value> time
    --soundsr=value - samplerate value (48000 by default)
    --soundenv=size - add a ramp envelop of size <size> at the beginning and the end of each evolution sequence
    --patternpos=X,Y - place the selected pattern at position X,Y

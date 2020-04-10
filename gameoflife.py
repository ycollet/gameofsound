# Python code to implement Conway's Game Of Life 
import argparse 
import math
import sys
import random
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import scipy.io.wavfile as wavf

import LIFReader

# setting up the values for the grid 
ON   = 255
OFF  = 0
vals = [ON, OFF] 

def randomGrid(N): 
        """returns a grid of NxN random values"""
        return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N) 

def addLine(i, j, grid, linesize):
        """adds a line of size 3 with top left cell at (i, j)"""
        grid[i:i+int(linesize), j] = 255 
    
def addRectangle(i, j, grid, rectanglesize):
        """adds a rectangle of size 10 by 10  with top left cell at (i, j)"""
        grid[i:i+int(rectanglesize), j:j+int(rectanglesize)] = 255 
    
def addCustom(i, j, grid, patternlist, infopattern):
        """adds a custom pattern  with top left cell at (i, j)"""
        offsetX = -int(infopattern['xmin'])
        offsetY = -int(infopattern['ymin'])
        for index in range(len(patternlist)):
                pattern = patternlist[index]
                posX = int(pattern['posX'])
                posY = int(pattern['posY'])
                        
                for index2 in range(len(pattern['pattern'])):
                        pat = pattern['pattern'][index2]
                        sizepat = len(pat)
                        print('at pos {} -> {}, {} = {}'.format(offsetX + posX + i, offsetX + posX + i + sizepat, offsetY + posY + j + index2, pat))
                        grid[offsetX + posX + i:offsetX + posX + i + sizepat, offsetY + posY + j + index2] = pat

def addGlider(i, j, grid): 
        """adds a glider with top left cell at (i, j)"""
        glider = np.array([[0, 0, 255], 
                           [255, 0, 255], 
                           [0, 255, 255]]) 
        grid[i:i+3, j:j+3] = glider 

def addGosperGliderGun(i, j, grid): 
        """adds a Gosper Glider Gun with top left 
        cell at (i, j)"""
        gun = np.zeros(11*38).reshape(11, 38) 

        gun[5][1] = gun[5][2] = 255
        gun[6][1] = gun[6][2] = 255

        gun[3][13] = gun[3][14] = 255
        gun[4][12] = gun[4][16] = 255
        gun[5][11] = gun[5][17] = 255
        gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
        gun[7][11] = gun[7][17] = 255
        gun[8][12] = gun[8][16] = 255
        gun[9][13] = gun[9][14] = 255

        gun[1][25] = 255
        gun[2][23] = gun[2][25] = 255
        gun[3][21] = gun[3][22] = 255
        gun[4][21] = gun[4][22] = 255
        gun[5][21] = gun[5][22] = 255
        gun[6][23] = gun[6][25] = 255
        gun[7][25] = 255

        gun[3][35] = gun[3][36] = 255
        gun[4][35] = gun[4][36] = 255

        grid[i:i+11, j:j+38] = gun 

def update(frameNum, img, grid, N): 
        global soundFile
        # copy grid since we require 8 neighbors 
        # for calculation and we go line by line 
        newGrid = grid.copy() 
        for i in range(N): 
                for j in range(N): 
                        # compute 8-neghbor sum 
                        # using toroidal boundary conditions - x and y wrap around 
                        # so that the simulaton takes place on a toroidal surface. 
                        total = int((grid[i, (j-1)%N]       + grid[i, (j+1)%N] +
                                     grid[(i-1)%N, j]       + grid[(i+1)%N, j] +
                                     grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                                     grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255) 

                        # apply Conway's rules 
                        if grid[i, j] == ON: 
                                if (total < 2) or (total > 3): 
                                        newGrid[i, j] = OFF 
                        else: 
                                if total == 3: 
                                        newGrid[i, j] = ON 

        # update data 
        img.set_data(newGrid) 
        grid[:] = newGrid[:]

        # update sound file
        global freqMin
        global freqMax
        global freqBin
        global sampleRate
        global soundEnv
        global time
        global exportSound

        if exportSound == True:
                soundData = np.zeros(int(time * sampleRate))
                freqData = np.zeros(N)
                #for i in range(N): 
                #        for j in range(N): 
                #                freqData[i] += grid[i, j]
                for i in range(N): 
                        freqData[i] = grid[i][:].sum()
                
                for t in range(int(time * sampleRate)):
                        soundData[t] += np.multiply(freqData, precompcos[t][:]).sum()
                
                for i in range(1,soundEnv):
                        soundData[-i] = soundData[-i] * 1.0 / float(soundEnv) * float(i)
                        soundData[i-1] = soundData[i-1] * 1.0 / float(soundEnv) * float(i)
                
                soundFile = np.concatenate((soundFile, soundData))
        
        print("Generation completed\n")
        
        return img, 

def process_options():
        # Command line args are in sys.argv[1], sys.argv[2] .. 
        # sys.argv[0] is the script name itself and can be ignored 
        # parse arguments 
        parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.") 

        # add arguments
        parser.add_argument('--grid-size', dest='N', required=False) 
        parser.add_argument('--mov-file', dest='movfile', required=False) 
        parser.add_argument('--interval', dest='interval', required=False) 
        parser.add_argument('--glider', action='store_true', required=False) 
        parser.add_argument('--gosper', action='store_true', required=False) 
        parser.add_argument('--rectangle', dest='rectanglesize', required=False) 
        parser.add_argument('--line', dest='linesize', required=False) 
        parser.add_argument('--custom', dest='custom', required=False) 
        parser.add_argument('--exportsound', action='store_true', required=False) 
        parser.add_argument('--soundfilename', dest='soundfilename', required=False) 
        parser.add_argument('--fmin', dest='fmin', required=False) 
        parser.add_argument('--fmax', dest='fmax', required=False) 
        parser.add_argument('--soundtime', dest='soundtime', required=False) 
        parser.add_argument('--soundsr', dest='soundsr', required=False) 
        parser.add_argument('--soundenv', dest='soundenv', required=False) 
        parser.add_argument('--patternpos', dest='patternpos', required=False) 
        args = parser.parse_args()
        
        global freqMin
        global freqMax
        global freqBin
        global sampleRate
        global soundEnv
        global time
        global exportSound
        global out_fn
        global N
        global patternpos
        
        # set grid size 
        N = 100
        if args.N and int(args.N) > 8: 
                N = int(args.N) 
        
        freqMin = float(100)
        if args.fmin:
                freqMin = float(args.fmin)

        freqMax = float(6000)
        if args.fmax:
                freqMax = float(args.fmax)

        out_fn = 'data.wav'
        if args.soundfilename:
                outfn = args.soundfilename

        exportSound = False
        if args.exportsound:
                exportSound = True

        time = 0.1
        if args.soundtime:
                time = float(args.soundtime)

        sampleRate = 48000
        if args.soundsr:
                sampleRate = float(args.soundsr)

        soundEnv = 1000
        if args.soundenv:
                soundEnv = int(args.soundenv)
        
        freqBin = float((freqMax - freqMin) / N)

        patternpos=(0,0)
        if args.patternpos:
                patternpos=eval(args.patternpos)
        
        if patternpos[0]<0 or patternpos[0]>N:
                print('pattern position X out of bounds: 0 <= {} <= {}'.format(patternpos[0],N))

        if patternpos[1]<0 or patternpos[1]>N:
                print('pattern position Y out of bounds: 0 <= {} <= {}'.format(patternpos[1],N))
        

        return args

# main() function 
def main(args):
        global N
        global patternpos
        
        # set animation update interval 
        updateInterval = 50
        if args.interval: 
                updateInterval = int(args.interval) 
        
        # declare grid 
        grid = np.array([]) 

        # check if "glider" demo flag is specified 
        grid = np.zeros(N*N).reshape(N, N) 
        if args.glider: 
                addGlider(patternpos[0], patternpos[1], grid) 
        elif args.gosper: 
                addGosperGliderGun(patternpos[0], patternpos[1], grid) 
        elif args.rectanglesize: 
                addRectangle(patternpos[0], patternpos[1], grid, args.rectanglesize) 
        elif args.linesize: 
                addLine(patternpos[0], patternpos[1], grid, args.linesize) 
        elif args.custom:
                pattern, infopattern = LIFReader.LIFReader(args.custom)
                sizeX = (infopattern['xmax'] - infopattern['xmin'])
                sizeY = (infopattern['ymax'] - infopattern['ymin'])
                
                if (sizeX > N):
                        print('Increase grid size. Size of pattern: {},{} / {}'.format(sizeX, sizeY, N))
                        sys.exit(1)
                
                if (sizeY > N):
                        print('Increase grid size. Size of pattern: {},{} / {}'.format(sizeX, sizeY, N))
                        sys.exit(1)
                
                addCustom(patternpos[0], patternpos[1], grid, pattern, infopattern) 
        else: # populate grid with random on/off - 
              # more off than on 
                grid = randomGrid(N) 
        
        # set up animation 
        fig, ax = plt.subplots() 
        img = ax.imshow(grid, interpolation='nearest') 
        ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), 
                                      frames = 10, 
                                      interval=updateInterval, 
                                      save_count=50) 
        
        # # of frames? 
        # set output file 
        if args.movfile: 
                ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264']) 
        
        plt.show() 

# call main 
if __name__ == '__main__':
        global exportSound
        global sampleRate
        global out_fn
        global precompcos
        global N
        
        args = process_options()
        
        if exportSound:
                soundFile = np.array(0, dtype='float64').reshape(1)

                print('Performing precomputation for audio\n')
                precompcos = np.zeros(N*int(sampleRate*time)).reshape(int(sampleRate*time),N)
                phase = np.random.uniform(0,1,1000) * 2.0 * math.pi
                for t in range(int(time * sampleRate)):
                        for i in range(N):
                                precompcos[t][i] = math.cos(2 * math.pi * (i*freqBin + freqMin) * float(t) / float(sampleRate) + phase[i])
        
        main(args)
        
        if exportSound:
                maxVal = np.amax(soundFile)
                soundFile = soundFile / maxVal / 2.0
                wavf.write(out_fn, sampleRate, soundFile)
        

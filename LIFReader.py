# http://plife.sourceforge.net/

# Content of a file:
# Life 1.05
# #D Switch Engine
# #D by Charles Corderman.
# #D The smallest forever-growing
# #D pattern in the Game of Life.
# #N
# #P -13 -3
# .*.*
# *
# .*..*
# ...***
# #P 13 2
# **
# *

def LIFReader(filename):
    fn = open(filename, 'r') 
    Lines = fn.readlines() 
    
    # Strips the newline character
    startPattern = False
    listPattern = [{'maxX': 0, 'maxY': 0, 'posX':0, 'posY':0, 'pattern': []}]
    index2 = 0
    maxX = 0
    maxY = 0
    maxPosX = 0
    maxPosY = 0
    minPosX = 1e6
    minPosY = 1e6
    for index in range(len(Lines)): 
        line = Lines[index].strip()
        
        if (line.startswith('#D') or line.startswith('#N') or line.startswith('#L')):
            continue
        
        # Get position
        if (not startPattern and line.startswith('#P')):
            posX = line.split('#P',1)[1].split(' ')[1]
            posY = line.split('#P',1)[1].split(' ')[2]
            startPattern = True
            pattern = None
            maxX = 0
            maxY = 0
            listPattern[index2]['posX'] = posX
            listPattern[index2]['posY'] = posY
            continue
        
        if startPattern and not line.startswith('#P'):
            patElem = []
            for elem in line:
                if (elem == '.'):
                    patElem.append(0)
                else:
                    patElem.append(255)

            if maxX < len(patElem):
                maxX = len(patElem)
            maxY += 1
            
            if minPosX>int(posX):
                minPosX = int(posX)
            if minPosY>int(posY):
                minPosY = int(posY)
            if maxPosX<int(posX):
                maxPosX = int(posX)
            if maxPosY<int(posY):
                maxPosY = int(posY)
            
            if pattern == None:
                pattern = [patElem]
            else:
                pattern.append(patElem)

        if (startPattern and (index == len(Lines)-1)):
            listPattern[index2]['pattern'] = pattern
            listPattern[index2]['maxX'] = maxX
            listPattern[index2]['maxY'] = maxY
            continue
        
        if (startPattern and (line.startswith('#P'))):
            listPattern[index2]['pattern'] = pattern
            listPattern[index2]['maxX'] = maxX
            listPattern[index2]['maxY'] = maxY
            maxX = 0
            maxY = 0
            listPattern.append({'maxX': 0, 'maxY': 0, 'posX':0, 'posY':0, 'pattern': []})
            index2 += 1
            posX = line.split('#P',1)[1].split(' ')[1]
            posY = line.split('#P',1)[1].split(' ')[2]
            listPattern[index2]['posX'] = posX
            listPattern[index2]['posY'] = posY
            startPattern = True
            pattern = None

    #for items in listPattern:
    #    for elem in items.items():
    #        print(elem)

    print('minPosX = {} maxPosX = {}'.format(minPosX, maxPosX))
    print('minPosY = {} maxPosY = {}'.format(minPosY, maxPosY))
    
    return listPattern

if __name__ == '__main__': 
    LIFReader('data/SWITCHEN.LIF')

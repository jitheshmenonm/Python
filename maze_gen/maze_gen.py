
import pygame
import random

sizeofBlock = 40
allBlocks = []
bStartGeneration = False
bStartSolving = False
currentX = 0
currentY = 0
targetX = 0
targetY = 0
visitedBlocks = []#list for backtracking
numberofColumns = (int)(800/sizeofBlock)
numberofRows = (int)(600/sizeofBlock)
bBackTracking = False

class CBlock2D:
    def __init__(self, posx, posy):
        self.m_posx = posx
        self.m_posy = posy       
        self.t = True
        self.r = True
        self.b = True        
        self.l = True
        self.m_bVisited = False
        self.m_distance = 0
    def xIndex(self):
        return self.m_posx
    def yIndex(self):
        return self.m_posy    
    def TopOn(self):
        return self.t
    def RightOn(self):
        return self.r
    def BottomOn(self):
        return self.b
    def LeftOn(self):
        return self.l
    def TopOff(self):
        self.t = False
    def RightOff(self):
        self.r = False
    def BottomOff(self):
        self.b = False
    def LeftOff(self):
        self.l = False
    def beenVisited(self):
        return self.m_bVisited
    def setVisited(self):
        self.m_bVisited = True
    def ResetVisited(self):
        self.m_bVisited = False
    def SetDistance(self, val):
        self.m_distance = val
    def GetDistance(self):
        return self.m_distance


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (255,   255,   0)
CYAN = (0, 255, 255)

pygame.init()

size = [800, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("maze gen")

done = False
clock = pygame.time.Clock()

def CreateBlocks():
    global allBlocks, sizeofBlock
    for i in range(0, 600, sizeofBlock):
        for j in range(0,800, sizeofBlock):
            allBlocks.append(CBlock2D(j,i))

def DrawBlocks():
    global allBlocks, visitedBlocks, sizeofBlock
    if bBackTracking==True:
        color2Use = RED
    else:
        color2Use = GREEN

    for cblock in allBlocks:        
        topCornerX = (cblock.xIndex())
        topCornerY = (cblock.yIndex())
        if cblock.TopOn()==True:
            pygame.draw.line(screen, BLUE, (topCornerX, topCornerY),(topCornerX+sizeofBlock, topCornerY), 2)#top
        if cblock.RightOn()==True:
            pygame.draw.line(screen, BLUE, (topCornerX+sizeofBlock, topCornerY), (topCornerX+sizeofBlock, topCornerY+sizeofBlock), 2)#right
        if cblock.BottomOn()==True:        
            pygame.draw.line(screen, BLUE, (topCornerX, topCornerY+sizeofBlock), (topCornerX+sizeofBlock, topCornerY+sizeofBlock), 2)#bottom
        if cblock.LeftOn()==True:
            pygame.draw.line(screen, BLUE, (topCornerX, topCornerY), (topCornerX, topCornerY+sizeofBlock), 2)#left
    
    for cblock2DrawCircle in visitedBlocks: 
        #find centre point and draw a circle
        topCornerX = (cblock2DrawCircle.xIndex())
        topCornerY = (cblock2DrawCircle.yIndex())
        centerx = topCornerX + (int)(sizeofBlock / 2)
        centery = topCornerY + (int)(sizeofBlock / 2)
        pygame.draw.circle(screen, color2Use, (centerx, centery), (int)(sizeofBlock/10))
    if bStartSolving == True:
        cbCurrent = GetMNthBlock(currentX, currentY)
        cbTarget = GetMNthBlock(targetX, targetY)
        #find centre point and draw a circle
        topCornerX = (cbCurrent.xIndex())
        topCornerY = (cbCurrent.yIndex())
        centerx = topCornerX + (int)(sizeofBlock / 2)
        centery = topCornerY + (int)(sizeofBlock / 2)
        pygame.draw.circle(screen, YELLOW, (centerx, centery), (int)(sizeofBlock/2))  
        topCornerX = (cbTarget.xIndex())
        topCornerY = (cbTarget.yIndex())
        centerx = topCornerX + (int)(sizeofBlock / 2)
        centery = topCornerY + (int)(sizeofBlock / 2)
        pygame.draw.circle(screen, CYAN, (centerx, centery), (int)(sizeofBlock/2)) 

def GetMNthBlock(m , n):
    global numberofColumns, nnumberofRows, sizeofBlock, allBlocks
    rowN = (int)(n/sizeofBlock)
    columnN = (int)(m/sizeofBlock)
    indextoaccess = rowN*numberofColumns + columnN
    if(indextoaccess > len(allBlocks)):
        assert(indextoaccess < len(allBlocks)),"Wrong index to access block!!"
    return allBlocks[indextoaccess]

def FindRandomUnvisitedNeighbour():
    global allBlocks, currentX, currentY, sizeofBlock
    nRandom = -1 #default
    newIndexX = -1
    newIndexY = -1
    triedTop = triedBottom= triedLeft= triedRight = False
    while ((newIndexX == -1 and newIndexY == -1) and (triedTop==False or triedBottom==False or triedLeft==False or triedRight==False)):
        nRandom = random.randint(1, 4)#1-t,2-b,3-r,4-l
        if nRandom == 1:#top
            triedTop = True
            newIndexX = currentX
            newIndexY = currentY-sizeofBlock
        elif nRandom == 2:#bottom
            triedBottom = True
            newIndexX = currentX
            newIndexY = currentY+sizeofBlock
        elif nRandom == 3:#right
            triedRight = True
            newIndexX = currentX+sizeofBlock
            newIndexY = currentY
        elif nRandom == 4:#left
            triedLeft = True
            newIndexX = currentX-sizeofBlock
            newIndexY = currentY

        if newIndexX < 0 or newIndexX > (800-sizeofBlock) or newIndexY < 0 or newIndexY > (600-sizeofBlock):
            newIndexX = newIndexY= -1
        else:
            cbNextcandidate = GetMNthBlock(newIndexX, newIndexY)
            if cbNextcandidate.beenVisited():
                newIndexX = newIndexY= -1
    
    if newIndexX == -1 and newIndexY == -1 and triedTop==True and triedBottom==True and triedLeft==True and triedRight==True:#tried all sides, still cant find a nearest member to move to. Do backtracking
       return None
    
    return (GetMNthBlock(currentX, currentY), GetMNthBlock(newIndexX, newIndexY), nRandom)

def RemoveWallBetweenCurrentAndSelected(cBlockCurrent, cBlockNext, nWhich):
    global allBlocks
    assert (1<= nWhich <=4),"Which Cell 2 remove!"
    if nWhich == 1:#top
        cBlockNext.BottomOff()
        cBlockCurrent.TopOff()            
    elif nWhich == 2:#bottom
        cBlockNext.TopOff()
        cBlockCurrent.BottomOff()
    elif nWhich == 3:#right
        cBlockNext.LeftOff()
        cBlockCurrent.RightOff()
    elif nWhich == 4:#left
        cBlockNext.RightOff()
        cBlockCurrent.LeftOff()    

def UpdateBlocks():
    global allBlocks, visitedBlocks, currentX,currentY, bBackTracking,bStartGeneration
    if bBackTracking == False:
        visitedBlocks.append(GetMNthBlock(currentX,currentY))#for backtracking
    tupData = FindRandomUnvisitedNeighbour()# uses currentX,currentY
    if tupData==None:
        bBackTracking = True
        GetMNthBlock(currentX,currentY).setVisited()
        if len(visitedBlocks)>0:
            visitedBlocks.pop() 
        if len(visitedBlocks)>0:#check size after poping
            currentX = visitedBlocks[-1].xIndex()
            currentY = visitedBlocks[-1].yIndex()
        else:
            bStartGeneration = False
    else:
        bBackTracking = False
        cBlock2Process = tupData[0]
        cBlockNext = tupData[1]
        nWhich = tupData[2]
        RemoveWallBetweenCurrentAndSelected(cBlock2Process, cBlockNext, nWhich)
        cBlock2Process.setVisited()    
        currentX = cBlockNext.xIndex()
        currentY = cBlockNext.yIndex()

def FindNextUnvisitedNearestNeighbour():
    global allBlocks, currentX, currentY, sizeofBlock
    nRandom = -1 
    newIndexX = -1
    newIndexY = -1
    triedTop = triedBottom= triedLeft= triedRight = False
    while ((newIndexX == -1 and newIndexY == -1) and (triedTop==False or triedBottom==False or triedLeft==False or triedRight==False)):
        nRandom = random.randint(1, 4)#1-t,2-b,3-r,4-l
        if nRandom == 1:#top
            triedTop = True
            newIndexX = currentX
            newIndexY = currentY-sizeofBlock
        elif nRandom == 2:#bottom
            triedBottom = True
            newIndexX = currentX
            newIndexY = currentY+sizeofBlock
        elif nRandom == 3:#right
            triedRight = True
            newIndexX = currentX+sizeofBlock
            newIndexY = currentY
        elif nRandom == 4:#left
            triedLeft = True
            newIndexX = currentX-sizeofBlock
            newIndexY = currentY

        if newIndexX < 0 or newIndexX > (800-sizeofBlock) or newIndexY < 0 or newIndexY > (600-sizeofBlock):#if outside bounds
            newIndexX = newIndexY= -1 # reset
        else:
            cbNextcandidate = GetMNthBlock(newIndexX, newIndexY)
            if cbNextcandidate.beenVisited():#if visited aready
                newIndexX = newIndexY= -1
            else: #check if there is wall in between 
                if((nRandom == 1 and cbNextcandidate.BottomOn()==True) or (nRandom == 2 and cbNextcandidate.TopOn()==True) or (nRandom == 3 and cbNextcandidate.LeftOn()==True) or (nRandom == 4 and cbNextcandidate.RightOn()==True)):
                    newIndexX = newIndexY= -1

    if newIndexX == -1 and newIndexY == -1 and triedTop==True and triedBottom==True and triedLeft==True and triedRight==True:#tried all sides, still cant find a nearest member to move to. Do backtracking
       return None
    
    return (GetMNthBlock(currentX, currentY), GetMNthBlock(newIndexX, newIndexY), nRandom)

def SolveMazeInSteps():
    global allBlocks, visitedBlocks, numberofColumns, numberofRows, bBackTracking, currentX,currentY
    if currentX == targetX and currentY == targetY:
        bStartSolving = False
        return
    if bBackTracking == False:
        visitedBlocks.append(GetMNthBlock(currentX,currentY))#for backtracking
    tupData = FindNextUnvisitedNearestNeighbour()# uses currentX,currentY
    if tupData==None:
        bBackTracking = True
        GetMNthBlock(currentX,currentY).setVisited()
        if len(visitedBlocks)>0:
            visitedBlocks.pop() 
        if len(visitedBlocks)>0:#check size after poping
            currentX = visitedBlocks[-1].xIndex()
            currentY = visitedBlocks[-1].yIndex()        
    else:
        bBackTracking = False
        cBlock2Process = tupData[0]
        cBlockNext = tupData[1]
        nWhich = tupData[2]
        cBlock2Process.setVisited()
        cBlockNext.SetDistance(cBlock2Process.GetDistance()+1)
        currentX = cBlockNext.xIndex()
        currentY = cBlockNext.yIndex()        

CreateBlocks()        

while not done: 
    clock.tick(10)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:       
                bStartGeneration = True
                #indexXY = random.randint(0, len(allBlocks)-1)
                #currentX = allBlocks[indexXY].xIndex()
                #currentY = allBlocks[indexXY].yIndex()
           elif event.key == pygame.K_UP:       
                for cblock in allBlocks:
                    cblock.ResetVisited()
                currentX = currentY = 0
                targetX = 800-sizeofBlock
                targetY = 600-sizeofBlock
                bStartSolving = True                

    screen.fill(BLACK)     
        
    if bStartGeneration == True:
       UpdateBlocks()

    if bStartSolving == True:
        SolveMazeInSteps()

    DrawBlocks()
       
    pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()





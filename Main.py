# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:12:30 2019

@author: Trinity
"""
#creating the board
import random
import copy
import time
"""
what's needed 
    - array for each stack
        - piles - 1 2D array?
        - stock - 1 1D array
        -foundation - 1D array of T/F
    - keep track of the what's flipped or not on a pile - 1 2D array  

3 parts of a deal:
    1.) tableau - 54 cards at beginning
        - 4 stacks of 5 cards facedown, 1 card faceup on each stack
        - 6 stacks of 4 cards facedown, 1 card faceup on each stack
    2.) foundation - 0 cards at beginning
        - where the stacks will be placed when one is completed
    3.) stock - 50 cards at beginning 
        - where any cards not in the tableau or foundation are

how the cards will be dealt to each stack 
    1.) table
    2.) foundation
"""
class Game:
    def __init__(self): #this creates the deck, unflipped board, and foundation
        self.deck=list(range(1,14))
        self.deck= self.deck*8
        self.unflipped=[[] for i in range(10)]
        random.shuffle(self.deck)
        for i in range(len(self.unflipped)):
            if i<4:
                self.unflipped[i]=(self.deck[0:6])
                del self.deck[0:6]
            else:
                self.unflipped[i]=(self.deck[0:5])
                del self.deck[0:5]
        self.foundation=self.deck
        self.stock=[]
        self.lines=['-','-','-','-','-','-','-','-','-','-']
        self.flipped=[[] for i in range(10)]
        self.InitialFlip()

    def InitialFlip(self): # does the intial flip
        for x in range(len(self.flipped)):
            self.flipped[x]=[self.unflipped[x][-1]]
            del self.unflipped[x][-1]

    def DisplayBoard(self):#displays the board vertically
        try:
            print("Stock --> " + str(len(self.foundation)//10))
            print()
            print ('\t'.join(str(x) for x in self.lines))
            print ('\t'.join(str(x) for x in self.stock))
            print()
            print ('\t'.join(str(len(x)) for x in self.unflipped))
            print()
            print ('\t'.join(str(x) for x in self.lines))
            print()
            upper = len(max(self.flipped, key=len)) # find longest sublist
            for i in range(upper):
                formatted_row = []
                for row in self.flipped:
                    try:
                        formatted_row.append(str(row[i]))
                    except IndexError:
                        formatted_row.append(" ")
                print('\t'.join(formatted_row))
            print()
            print ('\t'.join(str(x) for x in self.lines))
            print()            
        except:
            print("INVALID -- DISPLAY BOARD")

    #this function is really important, as it has to happen after every single move
    def FlipCard(self): #checks if a card needs to be flipped and if there is a card available to be flipped
        for i in range(len(self.flipped)):
            if not self.flipped[i] and self.unflipped[i]:
                self.flipped[i].append(self.unflipped[i].pop(0))

    def DealFoundation(self): #deals the foundation
        if not self.foundation:
            print()
            print("Sorry, there's no more cards in the stock")
            print()
        else:
            for x in range(len(self.flipped)):
                self.flipped[x].append(self.foundation[0])
                del self.foundation[0]

    def CheckCoordinateValidity(self,startX,startY,finishX):#checks if desired move is valid
        try:
            #checking the first coordinate
            return (0 <= startX < 10 and 0 <= finishX < 10) and (0 <= startY < len(self.flipped[startX]))
        except:
            print("INVALID -- COORDINATE VALIDITY")

    def CheckMoveValidity(self,startX,startY,finishX): #checks if the move is valid
        try:
            if len(self.flipped[finishX])==0:
                return True
            #check if the card at the target position is at the bottom of its stack
            elif len(self.flipped[finishX])>0:
                #check if the card at the current position is less than the card at the target position
                if self.OneLessThan(self.flipped[startX][startY],self.flipped[finishX][-1]):
                    #check if start card is on bottom
                    if startY == len(self.flipped[startX])-1:
                        return True
                    self.currentStack=self.flipped[startX][startY:]
                    if self.DecrementingByOne(self.currentStack):
                        return True
            return False
        except:
            print("INVALID -- MOVE VALIDITY")

    #checks if start card is one less than target card
    def OneLessThan(self, startCard, targetCard):
        return startCard == targetCard-1

    def DecrementingByOne(self, currentStack):
        for x in range(1,len(self.currentStack),1):
            if self.currentStack[x] == self.currentStack[x-1]-1:
                pass
            else:
                return False
        return True

    def MoveStack(self,startX,startY,finishX):#moves a card or stack
    #try:
        if startX == -1 and startY == -1 and finishX == -1:
            self.DealFoundation()
        #get the stack and remove it from start
        else:
            self.currentStack=[]
            self.GetStackOfCards(startX,startY,finishX)
            #move the stack to the new stack
            self.MoveToBottomOfTargetPile(self.currentStack,finishX)
        self.MoveToStock()
    #except Exception as e:
       # print("INVALID -- MOVE STACK")
       # print(str(e))


    def GetStackOfCards(self,startX,startY,finishX):
        try:
            if startY == len(self.flipped[startX])-1:
                self.currentStack.append(self.flipped[startX][startY])
                del self.flipped[startX][startY]
            else:
                self.currentStack=self.flipped[startX][startY:]
                del self.flipped[startX][startY:]
        except Exception as e:
            print("INVALID -- GET STACK OF CARDS")
            print(str(e))
            print(startX)
            print(startY)
            print(finishX)

    def MoveToBottomOfTargetPile(self, currentStack,finishX):
        for x in range(len(self.currentStack)):
            self.flipped[finishX].append(self.currentStack[x])    

    def StackCompleted(self,compare):
        for i in range(len(compare) - len(self.comparer) + 1):
            if self.comparer == compare[i:i+len(self.comparer)]: 
                return True
        return False

    def MoveToStock(self):
        try:
            self.stackCompleted=False
            self.completedRow=-1
            self.comparer = [13,12,11,10,9,8,7,6,5,4,3,2,1]
            for x in range(len(self.flipped)):
                if self.StackCompleted(self.flipped[x]):
                    self.stackCompleted=True
                    self.completedRow=x
            if self.stackCompleted:
                #add something to the stock
                self.stock.append("X")
                #remove the stack from flipped
                last= len(self.flipped[self.completedRow]) - 1 - self.flipped[self.completedRow][::-1].index(13)
                del self.flipped[self.completedRow][last:]    
            self.FlipCard()
        except: 
            print("INVALID -- MOVE TO STOCK")

    def CheckStock(self):
        return len(self.stock)==8

    def GetPossibleMoves(self):
        self.possibleMoves=[]
        for x in range(len(self.flipped)):
            if len(self.flipped[x]) == 0:
                continue
            else:
                for y in range(len(self.flipped[x])-1,-1,-1):
                    for z in range(len(self.flipped)):
                        if z == x:
                            continue
                        else:
                            self.currentList=[]
                            self.currentList.append(x)
                            self.currentList.append(y)
                            self.currentList.append(z)
                            self.possibleMoves.append(self.currentList)                
    
    def GetValidMoves(self):
        self.possibleValidMoves=[]
        for x in range(len(self.possibleMoves)):
            startX=self.possibleMoves[x][0]
            startY=self.possibleMoves[x][1]
            finishX=self.possibleMoves[x][2]
            if self.ValidMove(startX, startY, finishX):
                self.possibleValidMoves.append(self.possibleMoves[x])  

    def ValidMove(self, startX, startY, finishX):
        return self.CheckMoveValidity(startX,startY,finishX) and self.CheckCoordinateValidity(startX,startY,finishX)

def minimax(game, depth):
    c=1
    if depth == 0 or len(game.stock) ==6 or len(game.stock) ==7:
        return score(game),"",c
    value=-100000
    game.GetPossibleMoves()
    game.GetValidMoves()
    random.shuffle(game.possibleValidMoves)
    bestMove=[-100,-100,-100]
    for x in range(len(game.possibleValidMoves)):
        copy_game=copy.deepcopy(game)
        copy_game.MoveStack(game.possibleValidMoves[x][0],game.possibleValidMoves[x][1],game.possibleValidMoves[x][2])
        new_value,_,subcount= minimax(copy_game, depth-1)
        c+=subcount
        if value<=new_value:
            value=new_value
            bestMove=[]
            bestMove.append(game.possibleValidMoves[x][0])
            bestMove.append(game.possibleValidMoves[x][1])
            bestMove.append(game.possibleValidMoves[x][2])
    return value,bestMove,c

def score(game):
    
    totalScore=0
    unflippedCounter=0
    flippedCounter=0
    for x in range(10): 
        unflippedCounter+=len(game.unflipped[x])
        flippedCounter+=len(game.flipped[x])   
        if len(game.flipped[x]) == 0:
            totalScore+=100   
    totalScore=0+flippedCounter-(unflippedCounter+len(game.foundation))
    totalScore+=100*len(game.stock)
    return totalScore

def percentages(part,whole):
    return part/whole

def list_mean(n):
    
    summing = float(sum(n))
    count = float(len(n))
    if n == []:
        return False
    return float(summing/count)  
highestDepth = 5
gamesPlayed= 20
for y in range(1,highestDepth+1,1):
    outcomes=[]
    gameElapsedTime = []
    gameMoveTimes=[]
    gameCompletedStack=[]
    gameMovesMade=[]
    gameBoardsCompared=[]
    depth = y

    for x in range(gamesPlayed):
        print("Game: " + str(x+1))      
        g=Game()
        moves=[]
        scores=[]
        completedStacks=[]
        movesMade=[]
        boardsCompared=[]
        counter=0
        playingGame=True
        t = time.process_time()
        moveTimesCurrent=[]
        while playingGame:
            moveStart=time.process_time()
            completeMove=True
            scor,bestMove,count=minimax(g,depth)
            #print(count)
            if len(bestMove) == 0:
                #for x in range(10):
                    #print()
                #print("WOOO YOU WON")
                completedStacks.append(len(g.stock))
                movesMade.append(counter)
                outcomes.append("W")
                playingGame=False
                break
            repeated=False
            boardsCompared.append(count)
            startX = bestMove[0]
            startY = bestMove[1]
            finishX = bestMove[2]
            if startX == -100 or startY == -100 or finishX == -100:
                completeMove=False
            #if there are no available moves or the card youre moving from is the same as youre moving to
            #if the same move is made twice in 3 turns, deal the foundation
            moves.append(bestMove)
            scores.append(scor)
            if len(set(scores))==1:
                find=False
                dups = {tuple(x) for x in moves if moves.count(x)>1}
                if len(dups) >0:
                    if len(g.foundation) == 0:
                        print("Loss")
                        #print("Completed stacks: " + str(len(g.stock)))
                        #print("Moves made: " + str(counter))
                        outcomes.append("L")
                        #g.DisplayBoard()
                        playingGame=False
                        completedStacks.append(len(g.stock))
                        movesMade.append(counter)
                    else:
                        g.DealFoundation()
                        movesMade.append(counter)
                        completeMove=False
            if completeMove:
                g.MoveStack(startX,startY,finishX)
                counter+=1
            if len(moves) == 5:
                del moves[0]
            if len(scores) == 4 + (len(g.stock)*2):
                del scores[0]    
            if len(g.stock) == 6 or len(g.stock) == 7:
                #for x in range(10):
                    #print()
                print("WOOO YOU WON")
                completedStacks.append(len(g.stock))
                movesMade.append(counter)
                outcomes.append("W")
                playingGame=False
                break
            elapsedMoveTime=time.process_time()-moveStart
            moveTimesCurrent.append(elapsedMoveTime)
        gameMoveTimes.append(moveTimesCurrent)
        gameBoardsCompared.append(boardsCompared)
                
        elapsedTime = time.process_time() - t
        print("Elapsed time: " + str(elapsedTime))
        gameElapsedTime.append(elapsedTime)
        gameCompletedStack.append(completedStacks) 
        gameMovesMade.append(movesMade)



    print("==================================")
    losses=0
    wins=0

    for x in range(len(outcomes)):
        if outcomes[x] == 'L':
            losses+=1
        elif outcomes[x] == 'W':
            wins+=1

    averageTimesPerGame=[]  
    for x in range(len(gameMoveTimes)):
        averageTimesPerGame.append(list_mean(gameMoveTimes[x]))
    averagStacksPerGame=[]  
    for x in range(len(gameCompletedStack)):
        averagStacksPerGame.append(list_mean(gameCompletedStack[x]))
    averagMovesPerGame=[]  
    for x in range(len(gameMovesMade)):
        averagMovesPerGame.append(list_mean(gameMovesMade[x]))        
    averageBoardsPerGame=[]  
    for x in range(len(gameBoardsCompared)):
        averageBoardsPerGame.append(list_mean(gameBoardsCompared[x])) 
        
    print("Games played: " + str(gamesPlayed))
    print("Average time per game: " + str(list_mean(gameElapsedTime)))
    print("Average time per move per game: " + str(list_mean(averageTimesPerGame)))
    print("Average stacks completed per game: " + str(list_mean(averagStacksPerGame)))
    print("Average amount of boards compared: " + str(list_mean(averageBoardsPerGame)))
    print("Average moves per game: " + str(list_mean(averagMovesPerGame)))
    print("Depth: " + str(depth))
    print("Games won: " + str(wins))
    print("Games lost: " + str(losses))
    print("Win percentage: " + str(percentages(wins,len(outcomes))))
    print("Loss percentage: " + str(percentages(losses,len(outcomes))))
    print("==================================")

"""
how moves will work:
    -user gives the coordinates of the card they want to move and the card they want to move it to
    -checking validity
        -check if the coordinates are valid 
            -first coordinate has to between 0 and 9
            -second coordinate has to between 0 and the length of the row at the first corner-1
        -check if the move is valid
    -move the card(s) to the stack
    -flip any cards if necesary
"""

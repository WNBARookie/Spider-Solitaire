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
        self.foundation=[]
        for x in range(len(self.deck)):
            self.foundation.append(self.deck[x])
        self.stock=[]
        self.lines=['-','-','-','-','-','-','-','-','-','-']
        self.flipped=[[] for i in range(10)]
        self.gameList=[]
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
            if 0 <= startX < 10 and 0 <= finishX < 10:
                if 0 <= startY < len(self.flipped[startX]):
                    return True
                elif len(self.flipped[finishX]) == 0:
                    return True
                else: 
                    return False
            else:
                return False
        except:
            print("INVALID -- COORDINATE VALIDITY")
    def CheckMoveValidity(self,startX,startY,finishX): #checks if the move is valid
        try:
            """
            coordinates[0] = start x
            coordinates[1] = start y
            coordinates[2] = finish x 
            coordinates[3] = finish y -------REMOVE
            """
            if len(self.flipped[finishX])==0:
                return True
            #check if the card at the target position is at the bottom of its stack
            elif len(self.flipped[finishX])>0:
                #check if the card at the current position is less than the card at the target position
                if self.flipped[startX][startY] == self.flipped[finishX][-1]-1:
                    #check if all the cards that follow the card is one less than it
                    self.currentStack=[]
                    if startY == len(self.flipped[startX])-1:
                        return True
                    else:
                        for x in range(startY,len(self.flipped[startX]),1):
                            self.currentStack.append(self.flipped[startX][x])
                        #print(self.currentStack)
                        for x in range(1,len(self.currentStack),1):
                            #print("here " + str(x) + " " + str(self.currentStack))
                            if self.currentStack[x] == self.currentStack[x-1]-1:
                                #print("good")
                                pass
                            else:
                                return False
                        return True
                else:
                    return False
            else:
                return False
        except:
            print("INVALID -- MOVE VALIDITY")
    def MoveStack(self,startX,startY,finishX):#moves a card or stack
        try:
            if startX == -1 and startY == -1 and finishX == -1:
                self.DealFoundation()
            else:
                #get the stack
                self.currentStack=[]
                if startY == len(self.flipped[startX])-1:
                    self.currentStack.append(self.flipped[startX][startY])
                    del self.flipped[startX][startY]
                else:
                    for x in range(startY,len(self.flipped[startX]),1):
                        self.currentStack.append(self.flipped[startX][x])
                    del self.flipped[startX][startY:]
                #move the stack to the new stack
                #checks if the target list is empty
                if len(self.currentStack) == 1:
                    self.flipped[finishX].append(self.currentStack[0])
                else:
                    for x in range(len(self.currentStack)):
                        self.flipped[finishX].append(self.currentStack[x])
                self.MoveToStock()
        except:
            pass
            #print("INVALID -- MOVE STACK")
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
                for x in range(last-1,len(self.flipped[self.completedRow])-1,1):
                    del self.flipped[self.completedRow][-1]    
            self.FlipCard()
        except: 
            print("INVALID -- MOVE TO STOCK")
    def CheckStock(self):
        if len(self.stock)==8:
            return True
        else:
            return False      
    def GetPossibleMoves(self):
        """
        -go through the entire flipped board
        -start from the top(displayed as bottom)of the list and is actually the end of the list
        """
        self.possibleMoves=[]
        for x in range(len(self.flipped)):
            if len(self.flipped[x]) == 0:
                continue
            elif len(self.flipped[x]) == 1:
                #MAKE SOME MAGIC
                for y in range(len(self.flipped)):
                    self.currentList=[]
                    if y == x:
                        continue
                    else:
                        self.currentList.append(x)
                        self.currentList.append(0)
                        self.currentList.append(y)
                        self.possibleMoves.append(self.currentList)
            else:              
                for y in range(len(self.flipped[x])-1,-1,-1):
                    for z in range(len(self.flipped)):
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
            if self.CheckMoveValidity(startX,startY,finishX) and self.CheckCoordinateValidity(startX,startY,finishX):
                self.possibleValidMoves.append(self.possibleMoves[x])    


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
gamesPlayed= 5
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
            #if there are no available moves or the card youre moving from is the same as youre moving to
            #if the same move is made twice in 3 turns, deal the foundation
            moves.append(bestMove)
            scores.append(scor)
            if len(set(scores))==1:
                find=False
                dups = {tuple(x) for x in moves if moves.count(x)>1}
                if len(dups) >0:
                    if len(g.foundation) == 0:
                        #print("Loss")
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
                #print("WOOO YOU WON")
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

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:12:30 2019

@author: Trinity
"""
#creating the board
import random
import copy
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
        try:
            #get the stack and remove it from start
            self.currentStack=[]
            self.GetStackOfCards(startX,startY,finishX)
            #move the stack to the new stack
            self.MoveToBottomOfTargetPile(self.currentStack)
            self.MoveToStock()
        except:
            print("INVALID -- MOVE STACK")

    def GetStackOfCards(self,startX,startY,finishX):
        if startY == len(self.flipped[startX])-1:
            self.currentStack.append(self.flipped[startX][startY])
            del self.flipped[startX][startY]
        else:
            self.currentStack=self.flipped[startX][startY:]
            del self.flipped[startX][startY:]

    def MoveToBottomOfTargetPile(self, currentStack):
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

g=Game()

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
counter=0
while True:
    g.DisplayBoard()
    g.GetPossibleMoves()
    #for x in range(len(g.possibleMoves)):
        #print(g.possibleMoves[x])
    g.GetValidMoves()
    print()
    print("Total moves: " + str(counter))
    print()
    print("Possible moves: ")
    print()
    for x in range(len(g.possibleValidMoves)):
        print(str(x+1) + " " + str(g.possibleValidMoves[x]))
    print()
    print("Would you like to:\n 1 - Move a stack\n 2 - Deal the foundation")
    try:
        choice=int(input())
        if choice==1:
            move=int(input("Enter the # of which move you want to make: "))
            if 1 <= move < len(g.possibleValidMoves)+1:
                startX=g.possibleValidMoves[move-1][0]
                startY=g.possibleValidMoves[move-1][1]
                finishX=g.possibleValidMoves[move-1][2]
                g.MoveStack(startX,startY,finishX)
                counter+=1
            else:
                print("INVALID -- PICK ONE OF THESE NUMBERS")
        elif choice==2:
            g.DealFoundation()
        else:
            print("Invalid choice")
        if g.CheckStock():
            for x in range(10):
                print()
            print("Woo you won!")
            break
    except:
        print("INVALID INPUT")

print("Congratulations on this amazing achievement. Not many make it to this point")
print("Total moves: " + str(counter))

print("Congratulations on this amazing achievement. Not many make it to this point") 

print("Congratulations on this amazing achievement. Not many make it to this point") 

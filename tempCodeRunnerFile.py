        if startX == -1 and startY == -1 and finishX == -1:
            self.DealFoundation()
        #get the stack and remove it from start
        else:
            self.currentStack=[]
            self.GetStackOfCards(startX,startY,finishX)
            #move the stack to the new stack
            self.MoveToBottomOfTargetPile(self.currentStack)
        self.MoveToStock()
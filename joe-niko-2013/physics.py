'''
@author Joe Crozier & Niko Savas
'''
class Physics:
    def __init__(self, level):
        self.collisionRects = []
        self.levelRect = level.get_rect() #Rect of the level's bounds

    def bodyCanMoveToLocation(self, body, xOffset, yOffset):
        bodyRect = body.rect.copy() #Copy the body's rect (might not be necessary)
        proposedRect = bodyRect.copy() 
        proposedRect = proposedRect.move(xOffset, yOffset) #Proposed rect is where the body would move

        if self.levelRect.contains(proposedRect) and proposedRect.collidelist(self.collisionRects) == -1: #If proposedRect is inside the level, let it move 
            return True
        else:
            return False
    def addBody(self, rect):
        self.collisionRects.append(rect)

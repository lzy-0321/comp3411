# WaterNode test now
from nodeDefs import valueDefs as vd
from nodeDefs import node

class WaterNode(node.Node):
    # 1. bridgeMaxCapacity is 3; can't go beyond that
    # 2. bridgeType: SINGLE, DOUBLE, TRIPLE or just water
    # get functions as well I suppose

    # TO_REMOVE: bridge Capacity as it already exists
    bridgeMaxCapacity = vd.MAX_BRIDGE_CAPACITY
    # initial state
    bridgeType = vd.WATER
    # Horizontal variable: check to see if horizontal connection is possible
    horizontalCheck = True
    # Vertical variable: check to see if  vertical connection is possible
    verticalCheck = True

    # initialise waterNode
    def __init__(self, row, col):
        super().__init__(row, col, 0)
        # return self
    
    # return true if the capacity is less than max capacity; otherwise return false
    def bridgeCheck(self):
        return self.currCapacity < self.bridgeMaxCapacity
    
    # set the bridge type based on bridge made    
    def setBridge(self, numBridges, bridgeOrientation):
        # setting the bridge and also like. the capacity basically
        # um. this depends though hmm. maybe set it based on a thing that says its vertical or
        # horizontal
        if self.bridgeCheck() == False:
            print("No more!!!")
            # don't pass
            
        # DONE. maybe
        if bridgeOrientation == "horizontal":
            if numBridges == 1:
                self.bridgeType = vd.SINGLE_HORIZONTAL
                print("1")
            elif numBridges == 2:
                self.bridgeType =  vd.DOUBLE_HORIZONTAL
                print("2")
            elif numBridges == 3:
                self.bridgeType = vd.TRIPLE_HORIZONTAL
                print("3")
            pass
        else:
            if numBridges == 1:
                self.bridgeType = vd.SINGLE_VERTICAL
                print("1")
            elif numBridges == 2:
                self.bridgeType = vd.DOUBLE_VERTICAL
                print("2")
            elif numBridges == 3:
                self.bridgeType = vd.TRIPLE_VERTICAL
                print("3")
            pass
        self.setChecks()
        
    # just to set that no more bridges can be formed
    def setChecks(self):
        self.horizontalCheck = False
        self.verticalCheck = False

    # just to iterate capacity of the bridge   
    # def iterateCapacity(self):
    #     self.bridgeCapacity = self.bridgeCapacity - 1

    # getters: 
    # overriding the main function
    # def getCapacity(self):
    #     return super().getCapacity()
    
    # def getBridgeType(self): return self.bridgeType
    
    # for printing
    def printLook(self):
        return self.bridgeType
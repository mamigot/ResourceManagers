class Resource:

    def __init__(self, id, totUnits):
        self.id = id
        self.totUnits = totUnits

        self.availableUnits = totUnits
        self.busyUnits = 0


    def takeUnits(self, numUnits=1):
        if( numUnits <= self.availableUnits ):
            self.availableUnits -= numUnits
            self.busyUnits += numUnits
            return True

        else:
            return False

    def freeUnits(self, numUnits=1):
        if( self.availableUnits + numUnits <= self.totUnits ):
            self.availableUnits += numUnits
            self.busyUnits -= numUnits
            return True

        else:
            return False


    def getID(self):
        return self.id

    def getTotUnits(self):
        return self.totUnits

    def getNumAvailable(self):
        return self.availableUnits

    def getNumBusy(self):
        return self.busyUnits

    def __repr__(self):
        return str(str(self.getNumAvailable()) + " available units")

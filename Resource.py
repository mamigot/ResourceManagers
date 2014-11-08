class Resource:

    def __init__(self, id, numUnits):
        self.id = id
        self.numUnits = numUnits

        self.availableUnits = numUnits
        self.busyUnits = 0

    def takeUnit(self):
        if( self.availableUnits > 0 )
            self.availableUnits -= 1
            self.busyUnits += 1

    def freeUnit(self):
        if( self.availableUnits + 1 <= self.numUnits )
            self.availableUnits += 1
            self.busyUnits -= 1

    def getID(self):
        return self.id

    def getNumUnits(self):
        return self.numUnits

    def getNumAvailable(self):
        return self.availableUnits

    def getNumBusy(self):
        return self.busyUnits

    def __repr__(self):
        return str(self.__dict__)

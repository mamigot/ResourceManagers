class Resource:
    '''
    Gathers all data pertaining to resources and makes it available through
    a number of getters and setters. Note that a resource is mainly
    characterized by a unique ID and the number of units it holds.
    '''

    def __init__(self, id, totUnits):
        self.id = id # Uniquely identifies it
        self.totUnits = totUnits # Total units the resource has

        self.availableUnits = totUnits # Available units within the resource
        self.busyUnits = 0 # Non-available units within the resource


    def takeUnits(self, numUnits=1):
        '''
        Decrements the resource's count of available units (which increases
        its number of busy units)
        '''
        if( numUnits <= self.availableUnits ):
            self.availableUnits -= numUnits
            self.busyUnits += numUnits
            return True

        else:
            return False

    def freeUnits(self, numUnits=1):
        '''
        Decrements the resource's count of busy units (which increases
        its number of available units)
        '''
        if( self.availableUnits + numUnits <= self.totUnits ):
            self.availableUnits += numUnits
            self.busyUnits -= numUnits
            return True

        else:
            return False


    def getID(self):
        '''
        Gets the resource's ID
        '''
        return self.id

    def getTotUnits(self):
        '''
        Gets the resources's total number of units
        '''
        return self.totUnits

    def getNumAvailable(self):
        '''
        Gets the resource's total number of available units
        '''
        return self.availableUnits

    def getNumBusy(self):
        '''
        Gets the resource's total number of busy units
        '''
        return self.busyUnits

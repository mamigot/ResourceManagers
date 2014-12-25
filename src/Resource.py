class Resource:
    '''
    Gathers all data pertaining to resources and makes it available through
    a number of getters and setters. Note that a resource is mainly
    characterized by a unique ID and the number of units it holds.
    '''

    def __init__(self, id, totUnits):
        self.id = id # Uniquely identifies it
        self.numTotUnits = totUnits # Total units the resource has

        self.numAvailableUnits = totUnits # Available units within the resource
        self.numBusyUnits = 0 # Non-available units within the resource

    @property
    def id(self):
        '''
        Gets the resource's ID
        '''
        return self.id

    @property
    def numTotUnits(self):
        '''
        Gets the resources's total number of units
        '''
        return self.numTotUnits

    @property
    def numAvailableUnits(self):
        '''
        Gets the resource's total number of available units
        '''
        return self.numAvailableUnits

    @property
    def numBusyUnits(self):
        '''
        Gets the resource's total number of busy units
        '''
        return self.numBusyUnits


    def takeUnits(self, numUnits=1):
        '''
        Decrements the resource's count of available units (which increases
        its number of busy units)
        '''
        if( numUnits <= self.numAvailableUnits ):
            self.numAvailableUnits -= numUnits
            self.numBusyUnits += numUnits
            return True

        else:
            return False

    def freeUnits(self, numUnits=1):
        '''
        Decrements the resource's count of busy units (which increases
        its number of available units)
        '''
        if( self.numAvailableUnits + numUnits <= self.numTotUnits ):
            self.numAvailableUnits += numUnits
            self.numBusyUnits -= numUnits
            return True

        else:
            return False

class Instruction:
    '''
    Gathers all data pertaining to instructions and makes it available through
    a number of getters. Note that an instruction is characterized by
    the variables in its constructor.
    '''

    def __init__(self, command, taskID, delay, resourceType, numUnits):
        self.command = command # Initiate, request, release or terminate
        self.taskID = taskID # Task the instruction affects
        self.delay = delay # Determines when the instruction wants to "be run"
        self.resourceType = resourceType # Resource the instruction affects
        self.numUnits = numUnits # Number of units in given resource it affects

    @property
    def command(self):
        '''
        Gets the instruction's command
        '''
        return self.command

    @property
    def taskID(self):
        '''
        Gets the relevant task ID
        '''
        return self.taskID

    @property
    def delay(self):
        '''
        Gets the instruction's delay
        '''
        return self.delay

    @property
    def resourceType(self):
        '''
        Gets the relevant resource type
        '''
        return self.resourceType

    @property
    def numUnits(self):
        '''
        Gets the relevant number of units
        '''
        return self.numUnits

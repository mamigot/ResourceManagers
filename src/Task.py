class Task:
    '''
    Gathers all data pertaining to tasks and makes it available through
    a number of getters and setters. Note that a task is mainly characterized
    by a unique ID, a set of instructions and a state at a given point in
    time (active, waiting, aborted or finished).
    '''

    def __init__(self, id):
        self.id = id # Uniquely identifies it
        self.instructions = [ ] # Set of instructions in relevant order
        self.currInstruction = 0 # Used to iterate through instructions

        # State variables
        self.waiting = False
        self.finished = False
        self.aborted = False

        # Maps resource ID to count of units (relevant to Banker's algorithm)
        self.claims = {}

        # Maps resource ID to count of units
        self.heldResources = {}

        # Stats to measure runtime
        # ('running' is the time from initialization to end and 'waiting' is
        # time spent on the blocked list)
        self.stats = {'running':0, 'waiting':0}


    def isActive(self):
        '''
        Determines if the task is still relevant to the execution
        '''
        return not (self.isFinished() or self.isAborted())

    def isWaiting(self):
        '''
        True if waiting, false otherwise
        '''
        return self.waiting

    def isFinished(self):
        '''
        True if finished, false otherwise
        '''
        return self.finished

    def isAborted(self):
        '''
        True if aborted, false otherwise
        '''
        return self.aborted


    def wait(self):
        '''
        Marks task as 'waiting'
        '''
        self.waiting = True

    def stopWaiting(self):
        '''
        Tells task to stop waiting
        '''
        self.waiting = False

    def abort(self):
        '''
        Aborts the task and releases its resources
        '''
        self.releaseAllResources()
        self.stopWaiting()
        self.aborted = True


    def addInstruction(self, instruction):
        '''
        Adds an instruction to the task's list
        '''
        self.instructions.append( instruction )

    def incInstruction(self):
        '''
        Used as a 'pointer' to keep track of the next instruction
        '''
        if self.currInstruction < len(self.instructions) - 1:
            self.currInstruction += 1
        else:
            self.finished = True

    def incWaitingTime(self):
        '''
        Increments the time the task has been waiting
        '''
        self.stats['waiting'] += 1

    def clockEndTime(self, time):
        '''
        Marks time at which the task stopped executing
        '''
        self.stats['running'] = time


    def setClaims(self, resourceID, numUnits):
        '''
        Sets the task's claims from initialization
        (relevant to the banker's algorithm)
        '''
        self.claims[resourceID] = numUnits

    def getMaxAddl(self, resourceID=None):
        '''
        Gets maximum additional units for a resource, or all if no single
        resource is specified. Note that the max. additional resources are
        given by the (claims - heldResources).
        (This method is useful only if claims are set at initialization).
        '''
        if resourceID:
            if resourceID in heldResources.keys():
                return self.claims[resourceID] - self.heldResources[resourceID]
            else:
                return self.claims[resourceID]
        else:
            maxLeft = {rID:numUnits for rID, numUnits in self.claims.iteritems()}
            for rID in maxLeft.keys():
                if rID in self.heldResources.keys():
                    maxLeft[rID] -= self.heldResources[rID]
            return maxLeft


    def grantResource(self, resourceID, numUnits=1):
        '''
        Does not check if the resource actually has the units
        (that's the manager's job --this is just book-keeping)
        '''
        if( resourceID in self.heldResources.keys() ):
            # Already have at least one unit of this resource
            self.heldResources[resourceID] += numUnits
        else:
            self.heldResources[resourceID] = numUnits

    def releaseResource(self, resourceID, numUnits=1):
        '''
        Update records of currently held resources
        '''
        if( resourceID in self.heldResources.keys() ):
            self.heldResources[resourceID] -= numUnits

    def releaseAllResources(self):
        '''
        Empty the task's heldResources variable
        '''
        self.heldResources = {}


    def getID(self):
        '''
        Gets the task's ID
        '''
        return self.id

    def getClaims(self):
        '''
        Gets the tasks's claims
        '''
        return self.claims;

    def getAllInstructions(self):
        '''
        Gets the task's instructions
        '''
        return self.instructions

    def getCurrentInstruction(self):
        '''
        Uses the "current instruction pointer" to output the next
        relevant instruction in the task's list of instructions
        '''
        if( not self.isActive() or
            self.currInstruction >= len(self.instructions) ):
            return None

        return self.instructions[self.currInstruction]

    def getAllResources(self):
        '''
        Gets all of the task's resources
        '''
        return self.heldResources

    def getStats(self):
        '''
        Gets the task's stats (useful if the waiting time has been
        increased accordingly and that the end time was properly set)
        '''
        return self.stats


    def __repr__(self):
        '''
        Returns the task's ID as well as whether it's active and waiting
        '''
        info = "Task #" + str(self.getID()) + ": \n"
        info += "\tisActive(): " + str(self.isActive()) + "\n"
        info += "\tisWaiting(): " + str(self.isWaiting()) + "\n"
        return info

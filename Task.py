class Task:

    def __init__(self, id):
        self.id = id
        self.instructions = [ ]
        self.currInstruction = 0 # Used to iterate through instructions

        self.waiting = False
        self.finished = False
        self.aborted = False

        # Maps resource ID to count of units
        self.heldResources = {}

        # Stats to measure runtime
        self.stats = {'running':0, 'waiting':0}

    def isActive(self):
        return not (self.isFinished() or self.isAborted())

    def isWaiting(self):
        return self.waiting

    def isFinished(self):
        return self.finished

    def isAborted(self):
        return self.aborted

    def wait(self):
        self.waiting = True

    def stopWaiting(self):
        self.waiting = False

    def abort(self):
        self.releaseAllResources()
        self.stopWaiting()
        self.aborted = True

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
        if( resourceID in self.heldResources.keys() ):
            self.heldResources[resourceID] -= numUnits

    def releaseAllResources(self):
        self.heldResources = {}

    def addInstruction(self, instruction):
        self.instructions.append( instruction )

    def incInstruction(self):
        if self.currInstruction < len(self.instructions) - 1:
            self.currInstruction += 1
        else:
            self.finished = True

    def incWaitingTime(self):
        self.stats['waiting'] += 1

    def incRunningTime(self):
        self.stats['running'] += 1

    def getID(self):
        return self.id

    def getAllInstructions(self):
        return self.instructions

    def getCurrentInstruction(self):
        if( not self.isActive() or
            self.currInstruction >= len(self.instructions) ):
            return None

        return self.instructions[self.currInstruction]

    def getAllResources(self):
        return self.heldResources

    def getStats(self):
        return self.stats

    def __repr__(self):
        info = "Task #" + str(self.getID()) + ": \n"
        info += "\tisActive(): " + str(self.isActive()) + "\n"
        info += "\tisWaiting(): " + str(self.isWaiting()) + "\n"
        return info

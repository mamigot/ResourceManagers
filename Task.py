class Task:

    def __init__(self, id):
        self.id = id
        self.instructions = [ ]
        self.currInstruction = 0 # Used to iterate through instructions

        self.waiting = False
        self.finished = False
        self.aborted = False

        self.heldResources = {} # Maps resource ID to count of units


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

    def getID(self):
        return self.id

    def getAllInstructions(self):
        return self.instructions

    def getCurrentInstruction(self):
        if self.isFinished() or self.currInstruction >= len(self.instructions):
            self.finished = True; return

        return self.instructions[self.currInstruction]

    def getAllResources(self):
        return self.heldResources

    def __str__(self):
        return str(self.__dict__)

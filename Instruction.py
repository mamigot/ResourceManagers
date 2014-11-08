class Instruction:

    def __init__(self, command, taskID, delay, resourceType, numUnits):
        self.command = command
        self.taskID = taskID
        self.delay = delay
        self.resourceType = resourceType
        self.numUnits = numUnits

    def getCommand(self):
        return self.command

    def getTaskID(self):
        return self.taskID

    def getDelay(self):
        return self.delay

    def getResourceType(self):
        return self.resourceType

    def getNumUnits(self):
        return self.numUnits

    def __repr__(self):
        return str(self.__dict__)

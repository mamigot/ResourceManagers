class Instruction:

    def __init__(self, command, taskID, delay, resourceType, numUnits):
        self.command = command
        self.taskID = taskID
        self.delay = delay
        self.resourceType = resourceType
        self.numUnits = numUnits

    def getCommand():
        return self.command

    def __repr__(self):
        return str(self.__dict__)

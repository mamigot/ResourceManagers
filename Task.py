class Task:

    def __init__(self, id):
        self.id = id
        self.instructions = [ ]

        self.finished = False
        self.currInstruction = 0 # Used to iterate through instructions

    def isFinished(self):
        return self.finished

    def addInstruction(self, instruction):
        self.instructions.append( instruction )

    def getID(self):
        return self.id

    def getAllInstructions(self):
        return self.instructions

    def getCurrentInstruction(self):
        if self.isFinished() or self.currInstruction >= len(self.instructions):
            self.finished = True; return

        return self.instructions[self.currInstruction]

    def incInstruction(self):
        if self.currInstruction < len(self.instructions) - 1:
            self.currInstruction += 1
        else:
            self.finished = True

    def __str__(self):
        return str(self.__dict__)

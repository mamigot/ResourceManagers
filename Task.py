class Task:

    def __init__(self, id):
        self.id = id
        self.instructions = [ ]; # All but 'initiate'

    def addInstruction(self, instruction):
        self.instructions.append( instruction )

    def getID(self):
        return self.id

    def getInstructions(self):
        return self.instructions

    def __str__(self):
        return str(self.__dict__)

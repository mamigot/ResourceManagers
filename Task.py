class Task:

    def __init__(self, id):
        self.id = id

        # self.delay = delay
        # self.claims = claims
        # self.instructions = instructions;
        # # Next instruction pointer
        # self.nextInstr = 0

    def getNextInstruction():
        return self.instructions[self.nextInstr] # Check if this is valid

    def getID(self):
        return self.id

    def __str__(self):
        return "Task ID: " + str(self.id)

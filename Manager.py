import sys
import re

from Task import Task
from Resource import Resource
from Instruction import Instruction


tasks = {} # Maps task IDs to Task objects
resources = {} # Maps resource IDs to Resource objects



def parseInputData(outline, instructions):
    global tasks, resources # Modify the global variables
    tasks = {x:Task(x) for x in range(1, outline[0] + 1)}

    numResources = outline[1] + 1
    resources = {x:Resource(x, outline[x + 1]) for x in range(1, numResources)}

    pat = re.compile('\w+')
    for item in instructions:
        matches = pat.findall(item)

        command     = matches[0]
        taskID      = int(matches[1])
        delay       = int(matches[2])
        resourceType= int(matches[3])
        numUnits    = int(matches[4])

        ins = Instruction(command, taskID, delay, resourceType, numUnits)
        tasks[taskID].addInstruction( ins )



if __name__ == "__main__":
    filePath = "inputs/input-10.txt"
    file = file(filePath, 'r')

    outline = [int(s) for s in file.readline().split()]
    instructions = re.findall(r'[a-z]+\s+[\d\s]+', file.read())

    parseInputData(outline, instructions)

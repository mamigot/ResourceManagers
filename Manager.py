import sys
import re

from Task import Task
from Resource import Resource
from Instruction import Instruction


tasks = {} # Maps task IDs to Task objects
resources = {} # Maps resource IDs to Resource objects

sysClock = 0;

class ManagerType:
    '''
    Mimic enums
    '''
    OPTIMISTIC = 1
    BANKER = 2

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
        tasks[taskID].addInstruction(ins)

def isFinished():
    for task in tasks.values():
        if not task.isFinished() and not task.isAborted():
            return False
    return True

def isDeadlocked():
    '''
    Deadlock if all tasks are waiting
    '''
    for task in tasks.values():
        if not task.isWaiting():
            return False
    return True

def optimisticRequest(task, instruction):
    '''
    Fulfills the request if there are available resources
    '''
    resource = resources[instruction.getResourceType()]

    if( instruction.getNumUnits() <= resource.getNumAvailable() ):
        # The request can be fulfilled
        if( resource.takeUnits(instruction.getNumUnits()) ):
            task.grantResource(resource.getID(), instruction.getNumUnits())
            print("fulfilleddddd request")

    else:
        # Check if there's deadlock
        if( isDeadlocked() ):
            # Abort the task (+ free its resources)
            heldResources = task.getAllResources()
            for rID in heldResources.keys():
                resources[rID].freeUnits(heldResources[rID])

            task.abort()
            print("deadlock!")

        else:
            # Just have to wait until resources become available
            task.wait()



def execute(manager, task, instruction):
    if( instruction.getDelay() ):
        instruction.delay -= 1; return

    if( instruction.getCommand() == "initiate" and
        manager is ManagerType.BANKER ):
        print("Banker cares about the claims")

    if( instruction.getCommand() == "request" ):
        task.stopWaiting() # Assume it won't have to wait

        if( manager is ManagerType.OPTIMISTIC ):
            optimisticRequest(task, instruction)



    elif( instruction.getCommand() == "release" ):
        resource = resources[instruction.getResourceType()]

        if( instruction.getNumUnits() <= resource.getNumBusy() ):
            # The release can be fulfilled
            if( resource.freeUnits(instruction.getNumUnits()) ):
                task.releaseResource(resource.getID(), instruction.getNumUnits())
                print("fulfilled release")


    if( not task.isWaiting() )
        task.incInstruction()



def runManager():
    global sysClock

    while not isFinished():
        for task in tasks.values():
            if not task.isAborted() and not task.isFinished():
                ins = task.getCurrentInstruction()
                execute(ManagerType.OPTIMISTIC, task, ins)

        sysClock += 1


if __name__ == "__main__":
    filePath = "inputs/input-03.txt"
    file = file(filePath, 'r')

    outline = [int(s) for s in file.readline().split()]
    instructions = re.findall(r'[a-z]+\s+[\d\s]+', file.read())

    parseInputData(outline, instructions)

    runManager()

    print(sysClock)

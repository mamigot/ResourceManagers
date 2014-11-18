import sys
import re
import copy
from collections import OrderedDict

from Task import Task
from Resource import Resource
from Instruction import Instruction


# Read from input file
outline = []; instructions = []

# Maps all task IDs to all Task objects
tasks = {}
# Maps task IDs to waiting tasks (in order tasks were told to wait)
waitingTasks = OrderedDict()
# Tasks are placed here when they are freed from waiting
readyTasks = [] # (makes sure tasks are only processed once per cycle)

# Maps resource IDs to Resource objects
resources = {}
# Maps resource IDs to number of units that will be freed
freeBuffer = {}

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
        if( task.isActive() ):
            return False

    return True


def isDeadlocked():
    '''
    Deadlock if all active tasks are waiting
    '''
    for task in tasks.values():
        if( task.isActive() and not task.isWaiting() ):
            return False

    return not isFinished() # If it's finished, it's not deadlocked


def isSafe(task, instruction):
    '''
    Determines if a given task + instruction leads to a safe state.

    Dijkstra's algorithm to determine if a state is safe:
        1. State is safe if no tasks are left
        2. Look for task whose requests for all resources can be fulfilled
            -   If none exist, state is not safe
            -   Else: pretend to grant all resources to it, terminate it and
                continue to apply this method until all tasks are processed
    '''
    if isFinished(): return True

    # Abort task if it exceeds its claim
    if instruction.getNumUnits() > task.getMaxAddl()[instruction.getResourceType()]:
        if task.getID() in waitingTasks.keys():
            del waitingTasks[task.getID()]

        for rID in task.getAllResources().keys():
            placeIntoFreeBuffer(rID, task.getAllResources()[rID])

        task.abort()

        # Print informative message
        msg =   "During cycle " + str(sysClock) + "-" + str(sysClock+1)
        msg +=  " of Banker's algorithm\n"
        msg +=  "\tTask " + str(task.getID())
        msg +=  "'s request exceeds its claim; aborted; "
        msg +=  str(instruction.getNumUnits()) + " units available next cycle"
        print(msg)
        return False


    # Map resource ID to number of available units (copied structure)
    simResources = {rID:r.getNumAvailable() for rID, r in resources.iteritems()}
    # Map task ID to task object
    simTasks = {}
    for tID, t in tasks.iteritems():
        if t.isActive():
            simTasks[tID] = copy.deepcopy(t) # Copies full object

    # Pretend to grant the request
    wResourceID = instruction.getResourceType()
    wUnits = instruction.getNumUnits()
    simResources[wResourceID] -= wUnits
    simTasks[task.getID()].grantResource(wResourceID, wUnits)

    while simTasks: # There should be tasks available
        availTask = getFulfillableTask(simResources, simTasks)

        if availTask: # Free its resources and delete it
            for rID, units in availTask.getAllResources().items():
                simResources[rID] += units
            del simTasks[availTask.getID()]
        else:
            return False


    return True


def getFulfillableTask(maxResources, tasks):
    '''
    Returns a task whose max. additional request fits within the max. resources
    '''
    for task in tasks.values():
        resourceSet = task.getMaxAddl() # Maps resource ID to count of units
        isValid = True

        for rID in resourceSet.keys():
            if resourceSet[rID] > maxResources[rID]:
                isValid = False; break

        if isValid:
            return task

    return None


def getLowestDeadlockedTask():
    '''
    Has to be active, obviously
    '''
    for task in tasks.values():
        if( task.isWaiting() and task.isActive() ):
            return task

    return None


def resolveDeadlock():
    '''
    Abort the lowest numbered deadlocked task (+ free its resources)
    (repeat this process while there's deadlock)
    '''
    while( isDeadlocked() ):
        task = getLowestDeadlockedTask()
        if not task: return

        heldResources = task.getAllResources()
        for rID in heldResources.keys():
            placeIntoFreeBuffer(rID, heldResources[rID])

        del waitingTasks[task.getID()]
        task.abort()

        cleanFreeBuffer()

        for task in tasks.values():
            if task.isActive():
                ins = task.getCurrentInstruction()
                if(ins.getCommand() == "request"):
                    standardRequest(task, ins)
                    if( not task.isWaiting() ):
                        task.incInstruction()


def placeIntoFreeBuffer(resourceID, numUnits):
    global freeBuffer

    if( resourceID in freeBuffer.keys() ):
        freeBuffer[resourceID] += numUnits
    else:
        freeBuffer[resourceID] = numUnits


def cleanFreeBuffer():
    global freeBuffer

    for rID in freeBuffer.keys():
        resources[rID].freeUnits(freeBuffer[rID])
        del freeBuffer[rID]


def standardRequest(task, instruction):
    '''
    Fulfills the request if there are available resources
    '''
    if( instruction.getDelay() ):
        instruction.delay -= 1; return

    resource = resources[instruction.getResourceType()]

    if( instruction.getNumUnits() <= resource.getNumAvailable() ):
        task.stopWaiting() # Freed from waiting when request can be satisfied
        readyTasks.append(task) # Note that tasks were "readified" on this cycle

        if task.getID() in waitingTasks: # Leave the waiting tasks
            del waitingTasks[task.getID()]

        # The request can be fulfilled
        if( resource.takeUnits(instruction.getNumUnits()) ):
            task.grantResource(resource.getID(), instruction.getNumUnits())

    else:
        task.wait() # Wait until resources become available
        if not task.getID() in waitingTasks: # Enter the waiting tasks
            waitingTasks[task.getID()] = task


def bankerRequest(task, instruction):
    '''
    Wrapper around standardRequest() that proceeds only if the state is safe
    '''
    if isSafe(task, instruction):
        standardRequest(task, instruction)

    else:
        task.wait() # Wait until resources become available
        if not task.getID() in waitingTasks: # Enter the waiting tasks
            waitingTasks[task.getID()] = task


def bankerProcessClaims(task, initInstruction):
    '''
    Aborts task if it's asking for unknown resources or way too many units
    '''
    rType = initInstruction.getResourceType()
    rUnits = initInstruction.getNumUnits()

    if( not rType in resources.keys()
        or rUnits > resources[rType].getTotUnits() ):
        task.abort()

        # Print informative message
        msg =   "Banker aborts task " + str(task.getID()) + \
                " before run begins:\n"
        msg +=  "\tclaim for resource " + str(rType) + " (" + str(rUnits) + \
                ") exceeds number of units present (" + \
                str(resources[rType].getTotUnits()) + ")"
        print(msg)
    else:
        task.setClaims(rType, rUnits)


def execute(manager, task, instruction):
    if( instruction.getDelay() ):
        instruction.delay -= 1; return

    if( instruction.getCommand() == "initiate" and
        manager is ManagerType.BANKER ):
        bankerProcessClaims(task, instruction)

    if( instruction.getCommand() == "request" ):
        if( manager is ManagerType.OPTIMISTIC ):
            standardRequest(task, instruction)

        elif( manager is ManagerType.BANKER ):
            bankerRequest(task, instruction)


    elif( instruction.getCommand() == "release" ):
        resource = resources[instruction.getResourceType()]
        # Fulfill the release (place items into freeBuffer)
        if( instruction.getNumUnits() <= resource.getNumBusy() ):
            placeIntoFreeBuffer(resource.getID(), instruction.getNumUnits())
            task.releaseResource(resource.getID(), instruction.getNumUnits())

    # Carry on and determine stats
    if( not task.isWaiting() ):
        task.incInstruction()
        if task.isFinished():
            task.clockEndTime(sysClock)
    else:
        task.incWaitingTime()


def run(manager):
    global sysClock

    while not isFinished():
        global readyTasks

        # Process blocked tasks in the order they were told to wait
        for task in waitingTasks.values():
            if task.isActive(): # Should be all
                ins = task.getCurrentInstruction()
                execute(manager, task, ins)

        # Process non-blocked tasks
        for task in tasks.values():
            if( task.isActive() and not task.isWaiting()
                and not task in readyTasks ):
                ins = task.getCurrentInstruction()
                execute(manager, task, ins)

        readyTasks = [] # Reset ready tasks

        # Check if there's deadlock (applies to optimistic manager)
        if( manager is ManagerType.OPTIMISTIC and isDeadlocked() ):
            resolveDeadlock()

        cleanFreeBuffer()
        sysClock += 1


def simulateAlgorithm(manager):
    # Reset data structures
    global tasks, waitingTasks, readyTasks
    tasks = {}; waitingTasks = OrderedDict(); readyTasks = []

    global resources, freeBuffer
    resources = {}; freeBuffer = {}

    global sysClock
    sysClock = 0

    parseInputData(outline, instructions)
    run(manager)

    return assembleStats(tasks, manager)


def assembleStats(tasks, manager):
    '''
    Returns a dict mapping each task to a dict listing its statistics:
    time taken, waiting time, percentage of time spent waiting
    ex. (numerical keys denote task IDs aside from 'total')
        meta
            manager: "BANKER's"
        1
            taken: 9
            waiting: 4
            percentWaiting: 44
            aborted: False
        2
            taken: 0
            waiting: 0
            percentWaiting: 0
            aborted: True
        3
            taken: 7
            waiting: 3
            percentWaiting: 43
            aborted: False
        total
            taken: 16
            waiting: 7
            percentWaiting: 44
            aborted: False
    '''
    vals = {"taken":0, "waiting":0, "percentWaiting":0, "aborted":False}
    stats = {task.getID():copy.deepcopy(vals) for task in tasks.values()}

    # Individual tasks
    for taskID in stats.keys():
        if tasks[taskID].isAborted():
            stats[taskID]['aborted'] = True
            continue

        currStats = tasks[taskID].getStats()
        stats[taskID]['taken'] = currStats['running']
        stats[taskID]['waiting'] = currStats['waiting']
        stats[taskID]['percentWaiting'] = int(round(100.0 * \
            currStats['waiting'] / currStats['running']))

    # Totals
    totTaken = sum(ind['taken'] for ind in stats.values())
    totWaiting = sum(ind['waiting'] for ind in stats.values())

    stats['total'] = copy.deepcopy(vals) # Separate entry for cumulative data
    stats['total']['taken'] = totTaken
    stats['total']['waiting'] = totWaiting
    stats['total']['percentWaiting'] = int(round(100.0 * \
            stats['total']['waiting'] / stats['total']['taken']))

    # Set manager type
    stats['meta'] = {}
    if manager is ManagerType.OPTIMISTIC:
        stats['meta']['manager'] = 'OPTIMISTIC'
    elif manager is ManagerType.BANKER:
        stats['meta']['manager'] = 'BANKER\'S'

    return stats


def printReport(globalStats):
    report = "\n"
    report += "\t"*3 + "FIFO" + "\t"*6 + "BANKER's\n"
    for i in range(1, len(globalStats[0].keys()) - 1):
        report += "\t" + "Task " + str(i)

        report += "\t"*2
        if( globalStats[0][i]['aborted'] ):
            report += "aborted" + "\t"*4
        else:
            report += str(globalStats[0][i]['taken'])
            report += "\t"
            report += str(globalStats[0][i]['waiting'])
            report += "\t"
            report += str(globalStats[0][i]['percentWaiting']) + "%"
            report += "\t"*2


        report += "Task " + str(i)
        report += "\t"*2

        if( globalStats[1][i]['aborted'] ):
            report += "aborted" + "\t"*4
        else:
            report += str(globalStats[1][i]['taken'])
            report += "\t"
            report += str(globalStats[1][i]['waiting'])
            report += "\t"
            report += str(globalStats[1][i]['percentWaiting']) + "%"
            report += "\t"*2

        report += "\n"

    report += "\t" + "total"
    report += "\t"*2

    report += str(globalStats[0]['total']['taken'])
    report += "\t"
    report += str(globalStats[0]['total']['waiting'])
    report += "\t"
    report += str(globalStats[0]['total']['percentWaiting']) + "%"

    report += "\t"*2 + "total"
    report += "\t"*2

    report += str(globalStats[1]['total']['taken'])
    report += "\t"
    report += str(globalStats[1]['total']['waiting'])
    report += "\t"
    report += str(globalStats[1]['total']['percentWaiting']) + "%"
    report += "\t"*2

    report += "\n"
    print(report)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filePath = sys.argv[1]
    else:
        print("\nPlease restart the program and provide an input file.")
        print("ex.:\n\tpython2.7 Manager.py input-02.txt\n")
        exit(0)

    try: file = file(filePath, 'r')
    except IOError:
        print("\nCan't find: '" + filePath + "'.\n"); exit(0)


    outline = [int(s) for s in file.readline().split()]
    instructions = re.findall(r'[a-z]+\s+[\d\s]+', file.read())

    # Run for OPTIMISTIC and BANKER managers, and assemble stats
    globalStats = []

    globalStats.append( simulateAlgorithm(ManagerType.OPTIMISTIC) )
    globalStats.append( simulateAlgorithm(ManagerType.BANKER) )

    printReport(globalStats)

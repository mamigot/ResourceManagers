import sys
import re

from Task import Task

# Maps task IDs to respective objects
tasks = {}


def parseInputData(outline, instructions):
    tasks = { x:Task(x) for x in range(1, outline[0]) }

    print(tasks)


if __name__ == "__main__":
    filePath = "inputs/input-11.txt"
    file = file(filePath, 'r')

    outline = [int(s) for s in file.readline().split()]
    instructions = re.findall(r'[a-z]+\s+[\d\s]+', file.read())

    parseInputData(outline, instructions)

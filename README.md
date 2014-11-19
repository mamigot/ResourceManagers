Resource Managers
=================
**Miguel Amigot**
<br>
*Operating Systems, Fall 2014*


Implementation of the optimistic and Banker's algorithms for resource management using Python 2.7. The purpose of the program is to simulate the runtime behavior of each algorithm for a number inputs which specify the set of available resources as well as each task's set of instructions and demands.

Statistics are ultimately calculated and printed to the console (see [testResults.txt](testResults.txt) for the result of the provided inputs). The format of the output for each resource management algorithm is the following:

              Resource Management Algorithm
     Task 1      takenTime          waitingTime          percentWaiting
     ...
     total       totalTakenTime     totalWaitingTime     totalPercentWaiting

### Execute
To run the program for a single file, specify it as the first and only command line argument. See sample [input files](inputs/).
```
python2.7 Manager.py inputs/input-02.txt
```
In order to test the program for all given inputs, run the [tester.sh](tester.sh) Shell script as follows. Expected output: [testResults.txt](testResults.txt)
```
sh tester.sh
```

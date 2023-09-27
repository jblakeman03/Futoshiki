##EGR425
##Futoshiki Solver 

import numpy as np
import os
numbers = []
logic = []
solution = []
def main():
    numbers,logic,solution = ReadIn()
    print(numbers)
    print(logic)
    print(solution)
    initPop(numbers)


##Function to read in values and returns them in 2D Arrays  
def ReadIn():
    ##Get the file name for the numbers
    ##Will then switch letters to get desired logic and solution files 
    fileName = input('Input desired number file (ex. f4x4): ')
    numberFile = fileName + "n.txt"
    logicFile = numberFile.replace('n', 'l')
    solutionFile = numberFile.replace('n','s')

    nums = []
    log = []
    sol = []
    rows = 0
    logRows = 0

    f = open(numberFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        x = x.split(' ')
        nums.append(x)
        rows = rows+1
        
    f = open(logicFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        x = x.split(' ')
        log.append(x)
        logRows = logRows + 1
    f = open(solutionFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        x = x.split(' ')
        sol.append(x)

    nums = np.array(nums).reshape(rows,rows)
    log = np.array(log).reshape(logRows,4)
    sol = np.array(sol).reshape(rows,rows)


    return nums, log, sol

def initPop(nums):
    nums = np.array(nums)
    print(np.shape(nums))

 

main()



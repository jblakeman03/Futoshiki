##EGR425
##Futoshiki Solver 

import numpy as np
import random

numbers = []
logic = []
solution = []
def main():
    ##Gets arrays from read in 
    numbers,logic,solution = ReadIn()
    ##Create the initial population
    initPop(numbers)


##Function to read in values and returns them in 2D Arrays  
def ReadIn():
    ##Get the file name for the numbers
    ##Will then switch letters to get desired logic and solution files 
    ##fileName = input('Input desired number file (ex. f4x4): ')
    numberFile = 'f3x3' + "n.txt"
    logicFile = numberFile.replace('n', 'l')
    solutionFile = numberFile.replace('n','s')

    ##Initialize local temp array variables
    nums = []
    log = []
    sol = []
    rows = 0
    logRows = 0

    ##Opens number files, splits it by line, and adds it to a 1D array and keeps track of row count
    f = open(numberFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        x = x.split(' ')
        nums.append(x)
        rows = rows+1
        
    ##Opens Logic files, splits it by line, and adds it to a 1D array and keeps track of row count
    f = open(logicFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        x = x.split(' ')
        log.append(x)
        logRows = logRows + 1

    #Opens solution file, splits it by line, and adds it to a 1D array 
    f = open(solutionFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        x = x.split(' ')
        sol.append(x)

    ##uses row count and turns 1D array into 2D array for all arrays
    nums = np.array(nums).reshape(rows,rows)
    log = np.array(log).reshape(logRows,4)
    sol = np.array(sol).reshape(rows,rows)

    ##Returns temp arrays
    return nums, log, sol

##Creates the initial population with random values
def initPop(nums):
    ##Create copy of nums array and casts values as ints
    nums = np.array(nums, dtype= int)
    ##Gets number of rows and columns
    rows, col = np.shape(nums)
    ##Sets the population size
    popSize = 10
    ##Creates 3D array that holds individual elements that represent members of the popultion
    ##Loops through each 2D matrix and inserts a random value if there isnt a number given
    pop = np.zeros((popSize, rows, col))
    for i in range(popSize):
        for j in range(rows):
            for k in range(col):
                if(pop[i][j][k]==0):
                    pop[i][j][k] = random.randint(1,rows)   
    print(pop)

main()



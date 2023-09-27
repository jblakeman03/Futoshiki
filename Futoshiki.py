##EGR425
##Futoshiki Solver 

import numpy as np
import random
import math
import os

numbers = []
logic = []
solution = []
def main():
    ##Gets arrays from read in 
    numbers,logic,solution = ReadIn()
    ##Create the initial population
    initPop(numbers)
    max = max_score(number,logic)  
     
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

def reward(pop,c):
    #np.shape outputs the dimensions of an array (z,rows,columns)
    pop_dim = pop.shape #(# of agents,rows,columns)
    c_dim = c.shape #(# of constraints, 4)
    #'rewards' is a collection of 'reward' values bad naming i know
    #the z dimension value will correspond to a position in rewards
    rewards = np.zeros(pop_dim[0])
    #check each agent
    for z in range(pop_dim[0]):
        #start reward at 0 for each agent
        reward = 0
        #check rows
        for x in range(pop_dim[1]):
            #converts the list to set and then tests with original list if contains same no. of elements.
            #sets can not contain duplicate entries so if len(set())=len() all entries are unique
            if len(set(pop[z,x,:])) == len(pop[z,x,:]):
                reward = reward + 1
        #check columns
        for y in range(pop_dim[2]):
            if len(set(pop[z,:,y])) == len(pop[z,:,y]):
                reward = reward + 1
        #check constraints
        for i in range(c_dim[0]):
            if pop[z,c[i,0],c[i,1]]<pop[z,c[i,2],c[i,3]]:
                reward = reward + 2
        #print(reward)
        rewards[z] = reward
    return rewards

def max_score(board,c):
    #max score will be:
    #rows or columns*2 + number of constraints*(reward for having a constraint correct)
    #constraints give a bigger reward than having a row/column correct
    x = math.sqrt(board.size)
    c_dim = c.shape
    y = c_dim[1]
    total = (2*y)+(2*x)
    return total

def set(board,pop):
#np.nonzero indexs any nonzero values in the original board
#np.transpose groups output by element rather than dimension
    index = np.transpose(np.nonzero(board))
    pop_dim = pop.shape #3d
    index_dim = index.shape #2d
#will input given #'s to each agent
    for z in range(pop_dim[0]):
        # the number of given #'s is equal to the number of rows in index
        for x in range(index_dim[0]):
            #sets values in pop equal to values in board by index
            pop[z,index[x,0],index[x,1]]= board[index[x,0],index[x,1]]

    return pop


main()



##EGR425
##Futoshiki Solver 


=======
import os
import numpy as np
import math

numbers = []
logic = []
solution = []
def main():
    number,logic,solution = ReadIn()
    max = max_score(number,logic)   

##Function to read in values and returns them in 2D Arrays  
def ReadIn():
    ##Get the file name for the numbers
    ##Will then switch letters to get desired logic and solution files 
    fileName = input('Input desired number file: ')
    numberFile = fileName 
    logicFile = fileName.replace('n', 'l')
    solutionFile = fileName.replace('n','s')

    nums = []
    log = []
    sol = []

    f = open(numberFile, 'r')
    for line in f.readlines():
        nums.append(line.split(' '))

    f = open(logicFile, 'r')
    for line in f.readlines():
        log.append(line.split(' '))

    f = open(solutionFile, 'r')
    for line in f.readlines():
        sol.append(line.split(' '))

    return nums, log, sol


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

main()
=======



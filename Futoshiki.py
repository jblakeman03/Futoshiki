##EGR425
##Futoshiki Solver 

import numpy as np
import random
import math

numbers = []
logic = []
solution = []
def main():
    ##Gets arrays from read in and information from user 
    numbers,logic,solution = ReadIn()
    popSize = int(input('Enter desired population size: '))
    printFrequency = int(input('Print after how many generations (ex. 100): '))
    ##Max fitness is the highest fitness for the given board
    maxFitness = max_score(numbers,logic) 
    print()
    print('Initial Board:')
    printBoard(numbers,logic)
    print()
    print()

    ##Create the initial population
    pop = initPop(numbers, popSize)
    #haveSolution variable is used as sentinal and ends loop when solution is found
    haveSolution = False
    #Solution index represents the index of population array where solution is ofund
    solutionIndex = -1
    #genCount is the number of generations 
    genCount = 0
    #prevMax represents the max fintess score of the previous generation. This is used to determine if early convergence is happening
    prevMax = 0
    ##maxCounter is the number of times we have the previous generation has had the same fitness as the current one 
    maxCounter = 0
    ##numResets is the number of times we have increased the mutation rate 
    numResets = 0
    while(haveSolution == False):
        #Prob is the initial mutation rate 
        prob = 0.0005
        popFitness = reward(pop,logic)

        ##current best reprsents the highest fitness member in current population
        currentBest = np.argmax(popFitness)
        ##increase counter everytime we have repeat highest fitness 
        if(popFitness[currentBest]==prevMax):
            maxCounter = maxCounter + 1
        else: 
            prevMax = popFitness[currentBest]
        ##if we repeat 15 times increase mutation 
        if(maxCounter > 15): 
            maxCounter = 0
            numResets = numResets + 1
            prob = 0.75
        ##If increase mutation more than 5 times reset the population
        if((genCount % 1000)==0):
            pop = initPop(numbers, popSize)
            print('repop')
            numResets = 0
        ##Prints out data after a given amout of generations
        if((genCount%printFrequency)==0): 
            print('Current fitness: ', popFitness[currentBest])
            print('Generation: ', genCount)
            printBoard(pop[currentBest], logic)

        ##Solution index represents if we have a solution and if so where at
        solutionIndex = findSolution(popFitness,maxFitness)
        if(solutionIndex!=-1):
            haveSolution  = True
            print('Generation: ', genCount)
        ##If we dont have a solution go through basic GA steps
        if(haveSolution==False):
            selected = select(pop, popFitness, maxFitness)
            pop = reproduction(pop, selected,popFitness)
            pop = mutation(pop, prob)
            pop = performMutation(numbers,pop)
            genCount = genCount + 1

    print('Solution found!')
    printBoard(pop[solutionIndex], logic)



        
##Function to read in values and returns them in 2D Arrays  
def ReadIn():
    ##Get the file name for the numbers
    ##Will then switch letters to get desired logic and solution files 
    fileName = input('Input desired number file (ex. f4x4): ')
    numberFile =  fileName + "n.txt"
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
    nums = nums.astype(int)
    log = log.astype(int)
    sol = sol.astype(int)

    ##Returns temp arrays
    return nums, log, sol

##Function to print out board with logic symbols
##Basic approach is tp create an array with constraint rows between number rows and if there is a logic constraint put symbol between elements. 
##The iterate through each row, concatonate each element, then print the row
def printBoard(nums, log):
    nums = nums.astype(str)
    log = log.astype(str)
    ##get number of rows for numbers and logic arrays
    (numRows, numCol) = np.shape(nums)
    (logRows, logCol) = np.shape(log)

    ##Combined rows is the numbers plus constraints. Get the size by taking number of rows in numbers and adding one less than rows in numbers

    combinedRows = numRows + (numRows -1)
    combined = np.full((combinedRows,combinedRows),' ', dtype = str)
    ##Iterate through numbers and add them to their correct spot in combined array
    for i in range(numRows):
        for j in range(numCol):
            if(i==0 and j==0):
                combined[i][j] = str(nums[i][j])
            else:
                combined[2*i][2*j] = str(nums[i][j])
    ##Iterate through logic file and add constraints to correct spot in combined array
    for i in range(logRows):
        (x,y) = (int(log[i][0]),int(log[i][1]))
        (x2,y2) = (int(log[i][2]),int(log[i][3]))
        
        if((x==x2) and (y>y2)):
            combined[2*x][2*y-1] = '>'
        elif((x==x2) and (y<y2)):
            combined[2*x][2*y+1] = '<'
        elif((y==y2) and (x>x2)):
            combined[2*x-1][2*y] = 'v'
        elif((y==y2) and (x<x2)):
            combined[2*x+1][2*y] = '^'

    ##With all logic and numbers in correct locations, iterate through each row, concatonate elements together, and print each row.
    for i in range(combinedRows):
        row = ''
        for j in range(combinedRows):
            row = row + combined[i][j] + '   '
        print(row)



##Creates the initial population with random values
def initPop(nums, popSize):
    ##Create copy of nums array and casts values as ints
    nums = np.array(nums, dtype= int)
    ##Gets number of rows and columns
    rows, col = np.shape(nums)
    ##Sets the population size
    ##Creates 3D array that holds individual elements that represent members of the popultion
    ##Loops through each 2D matrix and inserts a random value if there isnt a number given
    pop = np.zeros((popSize, rows, col))
    for i in range(popSize):
        for j in range(rows):
            for k in range(col):
                if(pop[i][j][k]==0):
                    pop[i][j][k] = random.randint(1,rows)   
    return pop


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
                reward = reward + 2
        #check columns
        for y in range(pop_dim[2]):
            if len(set(pop[z,:,y])) == len(pop[z,:,y]):
                reward = reward + 2
        #check constraints
        for i in range(c_dim[0]):
            if pop[z,int(c[i,0]),int(c[i,1])]<pop[z,int(c[i,2]),int(c[i,3])]:
                reward = reward + 1
        #print(reward)
        rewards[z] = reward
    return rewards

def max_score(board,c):
    #max score will be:
    #rows or columns*2 + number of constraints*(reward for having a constraint correct)
    #constraints give a bigger reward than having a row/column correct
    x = math.sqrt(board.size)
    c_dim = c.shape
    y = c_dim[0]
    total = (1*y)+(4*x)
    return total


def performMutation(board,pop):
#np.nonzero indexs any nonzero values in the original board
#np.transpose groups output by element rather than dimension
    board = board.astype(int)
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

##Function that uses roulette wheel selection method to select parents from a population
def select(pop, popFitness, max):
    ##Sum variable used to sum all fitness scores of population together
    sum = 0
    for i in range(len(popFitness)):
        sum = sum + popFitness[i]

    ##SelectionProb holds probability of selection which is individual fitness score/sum of all fitness scores 
    selectionProb = []
    ##Selected holds the index of pop of chosen parent
    selected = []
    for i in range(len(popFitness)):
        selectionProb.append(popFitness[i]/sum)
    for i in range(len(popFitness)):
        selected.append([np.random.choice(len(popFitness),p=selectionProb)])
    return selected

def findSolution(popFitness, max):
    index = -1
    for i in range(len(popFitness)):
        if(popFitness[i]==max):
            index = i
    return index


def reproduction(pop, selected,rewards):
    #change selected parents matrix to a better shape [n,2]
    selected = np.reshape(selected, (int(len(selected)/2),2))
    #store dimension
    pop_dim = pop.shape
    #generate a new matrix with shape the same as pop
    #newPop = np.array(pop)
    newPop = np.zeros(pop.shape)
    count = 0 
    for i in range(len(selected)):
        #store 2 parents
        (p1,p2) = (selected[i][0], selected[i][1])
        #create two blank children matrix
        child1 = np.zeros([pop_dim[1],pop_dim[2]])
        child2 = np.zeros([pop_dim[1],pop_dim[2]])
        #flip a coin based on ratio of fitness of parents to determine the value of each cell
        #do same method twice because each set of parents creates 2 offspring
        for x in range(pop_dim[1]):
            for y in range(pop_dim[2]):
                if random.random()<(rewards[p1]/(rewards[p1]+rewards[p2])):
                    child1[x,y] = pop[p1,x,y]
                else:
                    child1[x,y] = pop[p2,x,y]
                if random.random()<(rewards[p1]/(rewards[p1]+rewards[p2])):
                    child2[x,y] = pop[p1,x,y]
                else:
                    child2[x,y] = pop[p2,x,y]
        #put newly generated children into newPop
        newPop[count] = child1
        newPop[count+1] = child2
        count += 2
    return newPop

## mutation method
def mutation(pop, prob):
    #go through every cell in pop and flip a coin to determine if mutation takes place
    pop_dim = pop.shape
    for z in range(pop_dim[0]):
        for x in range(pop_dim[1]):
            for y in range(pop_dim[2]):
                if random.random()<prob:
                    pop[z,x,y] = random.randint(1,pop_dim[1])
    return pop

     


main()



##EGR425
##Futoshiki Solver 


import os
numbers = []
logic = []
solution = []
def main():
    number,logic,solution = ReadIn()
    print(number)
    print(logic)
    print(solution)

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

    f = open(numberFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        nums.append(x)
        
    f = open(logicFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        log.append(x)

    f = open(solutionFile, 'r')
    for line in f.readlines():
        x = line
        x = x.strip()
        sol.append(x)

    return nums, log, sol


main()



##EGR425
##Futoshiki Solver 


=======
import os
numbers = []
logic = []
solution = []
def main():
    number,logic,solution = ReadIn()

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


main()
=======



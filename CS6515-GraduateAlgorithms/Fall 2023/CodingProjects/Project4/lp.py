# -*- coding: utf-8 -*-
"""
    lp.py       Intro to Graduate Algorithms

    ProjectLP, Fall 2023
    
    In this project you will utilize scipy.optimize.linprog to solve a linear program.
    The LP may be found in the project description.
"""

import argparse
from scipy.optimize import linprog
#you may NOT import any additional libraries/functions

def objectiveFunction():
    ''' Return the coefficients of the objective function as a list of values
        e.g.:  minimize -x - 2y would be represented as [-1, -2]'''
    # TODO Your code goes here
    c = [21, 16, 371, 346, 884]
    return c
    # TODone End of Your code

def constraintsA():
    ''' Return the coeffcients matrix A for the constraints.
        You should return a list of lists, e.g.: [ [1,2], [-1,0] ]'''
    # TODO Your code goes here
    a = [[-0.85, -1.62, -12.78, -8.39, 0], 
         [-0.33, -0.20, -1.58, -1.39, -100],
         [0.33, 0.20, 1.58, 1.39, 100],
         [-4.64, -2.37, -74.69, -80.70, 0],
         [9.00, 8.00, 7.00, 508.20, 0], 
         [-0.5, 0.5, 0.5, -0.5, -0.5]]
    return a
    # TODone End of Your code

def constraintsB():
    ''' Return the coeffcients vector B for the constraints
        You should return a one-dimensional list of values'''
    # TODO Your code goes here
    b = [-15, -2, 6, -4, 100, 0]
    return b
    # TODone End of Your code

def bounds():
    ''' return the lower & upper bounds for your variables
        You should return a one-dimensional list of tuples'''
    # TODO Your code goes here
    bounds = [(0, None), (0, None), (0, None), (0, None), (0, None)]
    return bounds
    # TODone End of Your code

#DO NOT MODIFY ANY CODE BELOW THIS LINE

def sciSolver():
    ''' Using linprog from scipy.optimize and the functions defined above, solve the LP
        You will return res, a scipy.optimize.OptimizeResult'''
    res = linprog(c=objectiveFunction(),
                  A_ub=constraintsA(),
                  b_ub=constraintsB(),
                  bounds=bounds())
    return res

def main():
    #DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    parser = argparse.ArgumentParser(description='Linear Programming Project')
    #use this flag, or change the default here to use different graph description files

    #args for autograder, DO NOT MODIFY ANY OF THESE
    parser.add_argument('-a', '--autograde',  help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2], default=1, dest='autograde')	
    args = parser.parse_args()
    
    #DO NOT MODIFY ANY OF THE FOLLOWING CODE

    res = sciSolver()
    print(res)

if __name__ == '__main__':
    main()
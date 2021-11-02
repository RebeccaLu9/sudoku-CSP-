############################################################
# CIS 521: Sudoku Homework 
############################################################

student_name = "Jingyi Lu"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
from copy import deepcopy
import collections

############################################################
# Section 1: Sudoku Solver
############################################################
def sudoku_cells():
    return [(row, col) for row in range(9) for col in range(9)]

def sudoku_arcs():
    arcs = []
    for rc1 in sudoku_cells():
        for rc2 in sudoku_cells():
            if rc1 != rc2:
                if (rc1[0] == rc2[0] or rc1[1] == rc2[1]):
                    arcs.append((rc1,rc2))
                elif (int(rc1[0]/3) == int(rc2[0]/3) and int(rc1[1]/3) == int(rc2[1]/3)):
                    arcs.append((rc1,rc2))
    return list(set(arcs))


def read_board(path):
#the read part get inspired by aayushidwivedi01 github
    dic = {}
    with open(path, 'r') as f:
        row = 0
        for line in f:
            col = 0
            for num in line.rstrip('\n'):
                if num == '*':
                    dic[(row, col)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                else:
                    dic[(row, col)] = set([int(num)])
                col += 1
            row += 1
    return dic

def sudoku_neighbors(arcs):
#the neighbors part get inspired by aayushidwivedi01 github
    d = dict();
    for (cell1, cell2) in arcs:
        if cell1 in d:
            d[cell1] += [(cell2, cell1)]
        else:
            d[cell1] = [(cell2, cell1)]
    return d

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    NEIGHBORS = sudoku_neighbors(ARCS)

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        set1=self.get_values(cell1)
        set2=self.get_values(cell2)
        if (len(set2) == 1 and len(self.get_values(cell1)) > 1):
        #if len(self.board[cell2]) == 1:
            for x in set1:
                if x in set2:
                    set1.remove(x)
                    cell1 = set(set1)
                    return True
            return False
        else:
            return False
        
    
    def infer_ac3(self):
        queue = collections.deque(Sudoku.ARCS)
        while len(queue) > 0:
            (cell1, cell2) = queue.pop()
            if self.remove_inconsistent_values(cell1, cell2):
                for arc in self.ARCS:
                    if cell1 in arc:
                        queue.append(arc)
        return self.board

    
    def infer_improved(self):
        made_addition_inference = True
        
        while made_addition_inference:
            self.infer_ac3()
            made_addition_inference = False
            
            for cell in Sudoku.CELLS:
                if(len(self.board[cell]) > 1): #not assigned yet
                    for value in self.board[cell]:
                        
                        neighbor = Sudoku.NEIGHBORS[cell]  
                        col = {val for s in [self.board[(i, cell[1])] for i in range(9) if (i, cell[1]) != cell] for val in s}
                        row = {val for s in [self.board[(cell[0], i)] for i in range(9)  if (cell[0], i) != cell] for val in s}            
                        block = {val for s in [self.board[(i,j)] for j in range(9) for i in range(9)\
                                        if (i, j) != cell and (i//3 == cell[0]//3) and (j//3 == cell[1]//3)] for val in s}
                        
                        if (value not in col) or (value not in row) or (value not in block):
                            made_addition_inference = True
                            self.board[cell] = set([value])
                            continue
        return

    
    def is_solved(self):
        for cell in self.CELLS:
            if len(self.board[cell]) != 1:
                return False
        return True
    
    def infer_with_guessing(self):
#         if self.is_solved():
#             return

        self.infer_improved()
        
        for cell in Sudoku.CELLS:
            if(len(self.board[cell]) > 1): #not assigned yet
                    for value in self.board[cell]:
                        copy = deepcopy(self)
                        copy.board[cell] = set([value])
                        copy.infer_with_guessing() #recursion
                        
                        if copy.is_solved():
                            self.board = copy.board
                            break
                    break
        
############################################################
# Section 2: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 15

feedback_question_2 = """
Debugging takes me really long.
"""

feedback_question_3 = """
It's fun game.
"""

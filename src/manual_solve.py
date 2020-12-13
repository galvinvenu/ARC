#!/usr/bin/python

# Student Name : Galvin Venugopal
# Student ID : 20235245
# github: https://github.com/galvinvenu/ARC

import os, sys
import json
import numpy as np
import re
from collections import Counter
import itertools

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation. 25d8a9c8

### c8cbb738 - Identify the most common color and the other colors. Identify the size of the output grid by finding the largest grid from the position of the other colors. 
### Create the out put grid and fill it with the most common color. for each of the other colors identify the relative position in the new output grid and set the colorts on those positions.   

def solve_c8cbb738(x):
    out_row_size =0
    out_col_size = 0
    # find unique colors in the grid and most common color in the grid
    SimpleList = itertools.chain.from_iterable(x)
    most_common_color = Counter(SimpleList).most_common(1)[0][0]   
    ls_unique_colors = np.unique(x)
    ls_unique_colors = ls_unique_colors[ls_unique_colors != most_common_color]
    ls_unique_colors_positions = []
    ls_unique_colors_size = []
    # identify the out shape and position and size of the colors that is not same as most common color
    for color in ls_unique_colors:
        sol = np.where(x == color)
        ls_unique_colors_positions.append(sol)
        row_size = (max(sol[0])-min(sol[0]))+1
        col_size = (max(sol[1])-min(sol[1]))+1  
        ls_unique_colors_size.append((row_size,col_size))          
        if out_row_size < row_size:
            out_row_size = row_size
        if out_col_size < col_size:
            out_col_size = col_size
    # create solution grid with most common color
    solution = np.full((out_row_size, out_col_size), most_common_color, dtype=int)
    # add unique colors to proper positions
    for positions, color, size in zip(ls_unique_colors_positions, ls_unique_colors, ls_unique_colors_size):
        min_row = min(positions[0])
        min_col = min(positions[1])
        for i,j in zip(positions[0],positions[1]):
            if size[0]==out_row_size:
                i -= min_row
            else:
                i = (i-min_row)+int(out_row_size/size[0])
            if size[1]==out_col_size:
                j -= min_col
            else:
                j = (j-min_col)+int(out_col_size/size[1])
            solution[i][j] = color
    return solution

### 1a07d186 - Identify the rows which has the same color and is not black. If no such row is found then transpose the grid and search if any columns exist with the same color. Once identified, find the individually present colors and their poistions. 
### If the individually found color is the same as the solid color rows, then move the individual point next to the solid color rows. depending on the side of the solid color row. 
### If the inidividual color point is below the solid color row then move it to the row below the solid color row , similarly the individual points qabove the solid color rows move it just above the solid color row. 
### If the matrix was transposed - transpose it back before returning it back to the caller 

def solve_1a07d186(x):
    same_color_rows_indexes = []
    same_color_rows_values = []
    ind_color_indexes = []
    ind_color_values = []
    same_color_row_exist =False
    x_transpose = False
    for i in x:
        if np.all(i==i[0]) and i[0] != 0:
            same_color_row_exist = True
            break
    
    if not same_color_row_exist:
        x_transpose = True
        
    if x_transpose:
        x = x.transpose()       

    rows, columns = x.shape

    for i in range(rows):
        if np.all(x[i]==x[i][0]) and x[i][0] != 0:
            same_color_rows_values.append(x[i][0])
            same_color_rows_indexes.append(i)
    for i  in range(rows):
        if i not in same_color_rows_indexes:
            for j in range (columns):
                if x[i][j] != 0:
                    ind_color_indexes.append((i,j))
                    ind_color_values.append(x[i][j])

    for i,v in zip(ind_color_indexes,ind_color_values):
        if v in same_color_rows_values:
            ind = same_color_rows_values.index(v)
            r_ind = same_color_rows_indexes[ind]
            if r_ind > i[0]:
                x[r_ind-1][i[1]] = v
                x[i[0]][i[1]] = 0
            else:
                x[r_ind+1][i[1]] = v
                x[i[0]][i[1]] = 0
        else:
            x[i[0]][i[1]] = 0

    if x_transpose:
        x = x.transpose()
    
    return x

### 9565186b - identify the most common color in the grid and convert all the others to Grey.

def solve_9565186b(x):
    SimpleList = itertools.chain.from_iterable(x)
    most_common_color = Counter(SimpleList).most_common(1)[0][0]   
    #change all the other to grey = 5
    x[x != most_common_color] = 5
    return x

### 25d8a9c8 - For each row check if the row is single colored, if yes - covert it to grey; else convert it to black

def solve_25d8a9c8(x):
    #identify rows with one color only, change to grey if same color, else black
    for i in range(x.shape[0]):
        result = np.all(x[i] == x[i][0])
        if result:
            x[i] = 5
        else:
            x[i] = 0
    return x


### 94f9d214 - Split the input into half. Identify the points where there is no color on both halfs. create a new out put 2Darray filled with 0s. 
### All the positions identified with no color, on both halves, update the solution matrix with color that is mean of 2 colors in the input

def solve_94f9d214(x):    
    ls_unique_colors = np.unique(x)
    ls_unique_colors = ls_unique_colors[ls_unique_colors != 0]
    newarr = np.vsplit(x, 2)
    output_shape = newarr[0].shape
    size = output_shape[0]*output_shape[1]
    sol = np.zeros(output_shape, dtype=int)
    positions = []
    
    for i,j,p in zip(newarr[0].flat[0:size],newarr[1].flat[0:size],np.arange(size)):
        if i == 0 and j==0:
            positions.append(p)
    
    for p in positions:
        sol.flat[p] = int(np.mean(ls_unique_colors))

    return sol


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()


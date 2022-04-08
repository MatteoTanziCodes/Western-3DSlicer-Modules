from sre_constants import BRANCH
from tkinter import HORIZONTAL
from vpython import *
from time import *
import random

##### Testing file #####

#### Main line segment ####
# Create main line segment vector
vector_array_main = [[0,0,0]]
branch_heads_array = []
MAIN_LINE_LENGTH = 80
BRANCH_AMOUNT_DIVISOR = 4
BRANCH_AMOUNT_UPPER = MAIN_LINE_LENGTH/BRANCH_AMOUNT_DIVISOR
AMOUNT_OF_BRANCHES = 0


def next_vector(vector_array, direction, index):
    prev_head = vector_array[index]

    new_x = random_number_increase(abs(prev_head[0]))
    new_y = random_number_increase(abs(prev_head[1]))
    new_z = random_number_increase(abs(prev_head[2]))

    if direction == "x":
        new_head = [round(prev_head[0],1),round(new_y,1),round(new_z,1)]
    elif direction == "y":
        new_head = [round(new_x,1),round(prev_head[1],1),round(new_z,1)]
    elif direction == "-y":
        new_head = [-1 * round(new_x,1),round(prev_head[1],1),round(new_z,1)]
    elif direction == "z":
        new_head = [round(new_x,1),round(new_y,1),round(prev_head[2],1)]
    elif direction == "-z":
        new_head = [-1 * round(new_x,1),round(new_y,1),round(prev_head[2],1)]
    return new_head

def random_number_increase(num):
    random_num = random.randint(1,20)
    random_num = random_num/10
    num = num + random_num
    return num

def create_main_line(vector_array_main):
    for x in range(MAIN_LINE_LENGTH):
        vector_array_main.append(next_vector(vector_array_main, "x", x))

def connect_main_line(vector_array_main):
    main_line = curve(vector_array_main[0],vector_array_main[1], color = color.red, radius = 0.5)
    main_line.append(vector_array_main)

def pick_branch_nodes(vector_array_main, branch_heads_array):
    AMOUNT_OF_BRANCHES = random.randint(BRANCH_AMOUNT_UPPER - 8,BRANCH_AMOUNT_UPPER)
    index_on_main_line = random.randint(2,BRANCH_AMOUNT_DIVISOR)
    for branch in range(AMOUNT_OF_BRANCHES):
        branch_heads_array.append(vector_array_main[index_on_main_line])
        index_on_main_line = index_on_main_line + random.randint(2,BRANCH_AMOUNT_DIVISOR)
    return branch_heads_array

def create_branches(branch_heads_array):
    amount_of_branches = len(branch_heads_array)
    branch_array = []
    for x in range(amount_of_branches):
        branch_array.append([])
        branch_array[x].append(branch_heads_array[x])
        direction = random.randint(1,4)
        if direction == 1:
            vector_direction = "y"
        elif direction == 2:
            vector_direction = "z"
        elif direction == 3:
            vector_direction = "-y"
        else:
            vector_direction = "-z"
        BRANCH_LENGTH = random.randint(8,25)
        for y in range(BRANCH_LENGTH):
            branch_array[x].append(next_vector(branch_array[x], vector_direction, y))
    return branch_array
            
def connect_branches(branch_array):
    array_of_branch_curves = []
    for x in range(len(branch_array)):
        array_of_branch_curves.append(curve(branch_array[x][0], branch_array[x][1], color = color.red, radius = 0.3))
        array_of_branch_curves[x].append(branch_array[x])

def create_target():
    random_x = random.randint(1,20)
    random_y = random.randint(1,20)
    random_z = random.randint(1,20)
    target = (random_x, random_y, random_z)
    return target

def bifurcation_points(branch_heads_array):
    return branch_heads_array

def centerline_points(vector_array_main):
    centerline_points_array = []
    index_on_main_line = random.randint(2,BRANCH_AMOUNT_DIVISOR)
    for branch in range(AMOUNT_OF_BRANCHES):
        centerline_points_array.append(vector_array_main[index_on_main_line])
        index_on_main_line = index_on_main_line + random.randint(2,BRANCH_AMOUNT_DIVISOR)
    return centerline_points_array

def point_transformation(vector):
    new_vector = []
    horizontal_translation = 5
    horizontal_stretch = 1/4
    z_stretch = 1.5

    new_vector.append((vector[0] + horizontal_translation) * horizontal_stretch)
    new_vector.append(vector[1])
    new_vector.append(vector[2] * z_stretch)
    return new_vector

def deform_vessel():
    


create_main_line(vector_array_main)
connect_main_line(vector_array_main)
pick_branch_nodes(vector_array_main, branch_heads_array, AMOUNT_OF_BRANCHES)
branch_array = create_branches(branch_heads_array)
connect_branches(branch_array)
CT_Target_registration = create_target()
bifurcation_points_array = bifurcation_points(branch_heads_array)
centerline_points_array = centerline_points(vector_array_main, AMOUNT_OF_BRANCHES)
US_Target_Registration = point_transformation(CT_Target_registration)



while True:
    pass

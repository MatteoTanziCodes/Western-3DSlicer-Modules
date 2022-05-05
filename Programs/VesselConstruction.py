import random

##### Testing file #####

#### Main line segment ####
# Create main line segment vector

MAIN_LINE_LENGTH = 40
BRANCH_AMOUNT_DIVISOR = MAIN_LINE_LENGTH / 8
BRANCH_AMOUNT_UPPER = MAIN_LINE_LENGTH/BRANCH_AMOUNT_DIVISOR
AMOUNT_OF_BRANCHES = 0
RANDOM_NUM_UPPER = BRANCH_AMOUNT_DIVISOR
RANDOM_NUM_LOWER = 1
RANDOM_NUM_DIVISOR = 10
X_TRANSLATION = 20
X_STRETCH = 1/4
Y_TRANSLATION = 0
Y_STRETCH = 1
Z_TRANSLATION = 0
Z_STRETCH = 3/2

def random_number_increase(num):
    random_num = random.randint(RANDOM_NUM_LOWER,RANDOM_NUM_UPPER)
    random_num = random_num/RANDOM_NUM_DIVISOR
    num = num + random_num
    return num

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


def create_main_line():
    vector_array_main = [[random.randint(0,3), random.randint(0,3), random.randint(0,3)]]
    for x in range(MAIN_LINE_LENGTH):
        vector_array_main.append(next_vector(vector_array_main, "x", x))
    return vector_array_main

def pick_branch_nodes(vector_array_main):
    branch_heads_array = []
    AMOUNT_OF_BRANCHES = random.randint(BRANCH_AMOUNT_UPPER,BRANCH_AMOUNT_UPPER)
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
            

def create_target():
    random_x = random.randint(5,40)
    random_y = random.randint(5,40)
    random_z = random.randint(5,40)
    target = (random_x, random_y, random_z)
    return target

def bifurcation_points(vessel):
    bifurcation_pts = []
    for x in range(len(vessel[0])):
        main_line_point = vessel[0][x]
        for y in range(len(vessel[1])):
            for z in range(len(vessel[1][y])):
                if vessel[1][y][z] == main_line_point:
                    bifurcation_pts.append(main_line_point)
    return bifurcation_pts

def centerline_points(vector_array_main):
    return vector_array_main

def point_transformation(vector):
    new_vector = []
    new_vector.append((vector[0] + X_TRANSLATION) * X_STRETCH)
    new_vector.append((vector[1] + Y_TRANSLATION) * Y_STRETCH)
    new_vector.append((vector[2] + Z_TRANSLATION) * Z_STRETCH)
    return new_vector

def deform_main_vessel(vector_array_main):
    deformed_main_array = []
    for x in range(len(vector_array_main)):
        deformed_main_array.append(point_transformation(vector_array_main[x]))
    return deformed_main_array

def deform_branches(branch_array):
    deformed_branch_array = []
    for x in range(len(branch_array)):
        deformed_branch_array.append([])
        for y in range(len(branch_array[x])):
            deformed_branch_array[x].append(point_transformation(branch_array[x][y]))
    return deformed_branch_array

def create_vessel():
    vessel = []
    vector_array_main = create_main_line()
    branch_array = create_branches(pick_branch_nodes(vector_array_main))
    vessel.append(vector_array_main)
    vessel.append(branch_array)
    return vessel

def create_deformed_vessel(vessel):
    deformed_main_array = deform_main_vessel(vessel[0])
    deformed_branch_array = deform_branches(vessel[1])
    vessel = []
    vessel.append(deformed_main_array)
    vessel.append(deformed_branch_array)
    return vessel

def Targets():
    targets = []
    CT_Target = create_target()
    US_Target = point_transformation(CT_Target)
    targets.append(CT_Target)
    targets.append(US_Target)
    return targets


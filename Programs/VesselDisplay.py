from vpython import *

def display_main_line(vector_array_main, color_choice):
    main_line = curve(vector_array_main[0],vector_array_main[1], color = color_choice, radius = 0.5)
    main_line.append(vector_array_main)

def display_branches(branch_array, color_choice):
    array_of_branch_curves = []
    for x in range(len(branch_array)):
        array_of_branch_curves.append(curve(branch_array[x][0], branch_array[x][1], color = color_choice, radius = 0.3))
        array_of_branch_curves[x].append(branch_array[x])

def display_point(point, color_choice, rad):
    points(point, radius = rad, color =  color_choice)

# def transform(main_vessel, deform_vessel_start, deform_vessel_finish, fiducials_start, fiducials_finish, target_start, target_finish):

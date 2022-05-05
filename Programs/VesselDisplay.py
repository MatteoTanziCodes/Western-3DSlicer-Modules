from vpython import *

def display_main_line(vector_array_main, color_choice):
    main_line = curve(vector_array_main[0],vector_array_main[1], color = color_choice, radius = 0.3)
    main_line.append(vector_array_main)

def display_branches(branch_array, color_choice):
    array_of_branch_curves = []
    for x in range(len(branch_array)):
        array_of_branch_curves.append(curve(branch_array[x][0], branch_array[x][1], color = color_choice, radius = 0.1))
        array_of_branch_curves[x].append(branch_array[x])

def display_point(point, color_choice, rad):
    points(pos = point, radius = rad, color =  color_choice)

def display_points(points, color_choice, rad):
    for x in range(len(points)):
        vec = vector(points[x][0], points[x][1], points[x][2])
        display_point(vec, color_choice, rad)

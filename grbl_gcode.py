#import numpy as np

def generate_path_gcode(transformed_path, feed_rate, coorinadte_transform = None):
    #print(len(transformed_path[0][0][0]))
    for i in range(len(transformed_path[0])):
        xcoord = transformed_path[0][i][0][0]
        ycoord = transformed_path[0][i][0][1]
        next_line = 'G01 X{} Y{} Z0 F{}\n'.format(xcoord,ycoord,feed_rate)
        print(next_line)
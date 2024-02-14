#import numpy as np
#https://www.simplify3d.com/resources/articles/3d-printing-gcode-tutorial/


def generate_path_gcode(transformed_path,ratio, feed_rate, mm_to_px_ratio = None):
    #print(len(transformed_path[0][0][0]))
    with open('newgcode.txt', 'w') as file:
        file.write('G17 G21 G90 G94 G54\nG00 X{} Y{} Z5\n'.format(ratio*transformed_path[0][0][0][0],ratio*transformed_path[0][0][0][1]))
        
        for i in range(len(transformed_path[0])):
            xcoord = ratio*transformed_path[0][i][0][0]
            ycoord = ratio*transformed_path[0][i][0][1]
            file.write('G01 X{} Y{} Z0 F{}\n'.format(xcoord,ycoord,feed_rate)) 
        
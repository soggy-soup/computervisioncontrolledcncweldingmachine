import numpy as np
#https://www.simplify3d.com/resources/articles/3d-printing-gcode-tutorial/


def generate_path_gcode(transformed_path,ratio, feed_rate, mm_to_px_ratio = None):
    #print(len(transformed_path[0][0][0]))
    with open('newgcode.txt', 'w') as file:
        file.write('G17 G21 G90 G94 G54\nG01 X{} Y{} Z5 F{}\n'.format(ratio*transformed_path[0][0][0][0],ratio*transformed_path[0][0][0][1],feed_rate))
        
        for i in range(len(transformed_path[0])):
            xcoord = np.around(ratio*transformed_path[0][i][0][0],5)
            ycoord = np.around(ratio*transformed_path[0][i][0][1],5)
            file.write('X{} Y{} Z0\n'.format(xcoord,ycoord)) 
        
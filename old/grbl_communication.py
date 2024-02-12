import serial
import time
import numpy as np






def generate_path_gcode(transformed_path, feed_rate, coorinadte_transform = None):
    print(len(transformed_path[0][0][0]))
    for i in range(len(transformed_path[0])):
        xcoord = transformed_path[0][i][0][0]
        ycoord = transformed_path[0][i][0][1]
        next_line = 'G01 X{} Y{} 100\n'.format(xcoord,ycoord)
        print(next_line)
generate_path_gcode(np.load('INTERSECTION.npy'), None,None)


#s = serial.Serial('/dev/tty.usbmodem1811',115200)

#file = open("gcode.gcode", 'r')

#s.write("\r\n\r\n")
#time.sleep(3)
#s.flushInput()

#for line in file:
    




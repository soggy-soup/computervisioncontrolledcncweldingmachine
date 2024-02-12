import cv2
import numpy as np
from util_funcs import displayimg



def radius_intersect(cont1, cont2, radius = None):
    rad_squared = radius ** 2
    print("CONT1",cont1[0][0][0])
    cont1 = cont1.squeeze()
    cont2 = cont2.squeeze()
        
    deltas = cont1[:,None,:] - cont2[None,:,:]
    distances = np.sum(np.square(deltas), axis = -1)
       
    overlap = np.flatnonzero(distances <= rad_squared)
    idx_delete = np.unravel_index(overlap,distances.shape)
        
    cont1 = np.delete(cont1, idx_delete[0], 0)
    cont2 = np.delete(cont2, idx_delete[1], 0)
    cont1 = cont1[None,:,None]
    cont2 = cont2[None,:,None]
    testimg = cv2.imread("images\\both_w_tag.jpg")
    newjoint = cv2.drawContours(testimg, cont2, -1, (0, 0, 255), thickness = 15)
    displayimg.img_show(newjoint)
    np.save('INTERSECTION.npy',cont2)
    
    

test1 = np.load('contours1.npy')
test2 = np.load('contours2.npy')

#test1 = np.array([[100,100], [100,300],[100,600]]) 
#test2 = np.array([[100,105], [200,300],[200,600],[200,800]])

radius_intersect(test1,test2,radius = 25)

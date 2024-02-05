import cv2
import numpy as np
from util_funcs import displayimg



def radius_intersect(cont1, cont2, radius = None):
    rad_squared = radius ** 2
    cont1 = cont1.squeeze()
    cont2 = cont2.squeeze()
    print(cont1)
    print(cont2)
    
    deltas = cont1[:,None,:] - cont2[None,:,:]
    distances = np.sum(np.square(deltas), axis = -1)
    print(distances)
    
    overlap = np.flatnonzero(distances <= rad_squared)
    idx_delete = np.unravel_index(overlap,distances.shape)
    
    print(idx_delete[0])
    
    cont1 = np.delete(cont1, idx_delete[0], 0)
    cont2 = np.delete(cont2, idx_delete[1], 0)
    cont1 = cont1[None,:,None]
    cont2 = cont2[None,:,None]
    
    
    
    
    
    
    
    



#test1 = np.load('test1contours.npy')
#test2 = np.load('test2contours.npy')

test1 = np.array([[1,1], [1,2],[1,3]]) 
test2 = np.array([[1,2], [1,5],[1,6],[1,7]])

radius_intersect(test1,test2,radius = 1)

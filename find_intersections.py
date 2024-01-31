import cv2
import numpy as np
from util_funcs import displayimg


def find_intersection(img1_contours, img2_contours):
    img1nooverlap = []
    img2nooverlap = []
    img1points = np.concatenate(img1_contours, axis=1)
    img1points = img1points.reshape(-1, img1points.shape[-1])
    img2points = np.concatenate(img2_contours, axis=1)
    img2points = img2points.reshape(-1, img2points.shape[-1])

    for index1,points1 in enumerate(img1points):
        for index2,points2 in enumerate(img2points):
            if np.array_equal(points1,points2):
                #print('test')
                img1nooverlap = np.delete(img1points, index1, axis = 0)
                img2nooverlap = np.delete(img2points, index2, axis = 0)
                
   
    img1nooverlap = img1nooverlap.reshape(len(img1nooverlap), 1, 2)
    img2nooverlap = img2nooverlap.reshape(len(img2nooverlap), 1, 2)
    
    asdf = cv2.drawContours(cv2.imread('images\\background.jpg'), img2nooverlap, -1, (0, 0, 255), 4)
    displayimg.img_show(asdf)
    
    
    

    
  
#test1 = np.array([[[[1, 2]], [[4, 2]], [[6, 7]]]])  
test1 = np.load('test1contours.npy')

#test2 =np.array([[[[1, 3]], [[7, 4]], [[6, 7]]]])
test2 = np.load('test2contours.npy')

find_intersection(test1,test2)


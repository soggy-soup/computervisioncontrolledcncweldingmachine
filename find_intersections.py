import cv2
import numpy as np


def find_intersection(img1_contours, img2_contours):
    img1points = np.concatenate(img1_contours, axis=1)
    img1points = img1points.reshape(-1, img1points.shape[-1])
    img2points = np.concatenate(img2_contours, axis=1)
    img2points = img1points.reshape(-1, img2points.shape[-1])
        
    for points1 in img1points:
        for points2 in img2points:
            if np.array_equal(points1,points2):
                print(points1,points2)
    
   # print(img1points)
   # print(img2points)
    
  
#test1 = np.array([[[[1, 3]], [[4, 5]], [[6, 7]]]])  
test1 = np.load('test1contours.npy')

#test2 =np.array([[[[1, 3]], [[4, 5]], [[6, 7]]]])
test2 = np.load('test2contours.npy')



find_intersection(test1,test2)


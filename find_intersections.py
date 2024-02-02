import cv2
import numpy as np
from util_funcs import displayimg

#https://stackoverflow.com/questions/55641425/check-if-two-contours-intersect
#https://docs.opencv.org/4.x/d8/d34/group__cudaarithm__elem.html
#https://docs.opencv.org/4.x/d1/d1c/classcv_1_1ximgproc_1_1EdgeDrawing.html
#https://answers.opencv.org/question/37392/how-to-compute-intersections-of-two-contours/

def find_intersection(img1_contours, img2_contours, dist=None):
    img1points = np.concatenate(img1_contours, axis=1)
    img1points = img1points.reshape(-1, img1points.shape[-1])
    img2points = np.concatenate(img2_contours, axis=1)
    img2points = img2points.reshape(-1, img2points.shape[-1])
    img1nooverlap = img1points.copy()
    img2nooverlap = img2points.copy()
    
    for index1,points1 in enumerate(img1points):
        
        for index2,points2 in enumerate(img2points):
            
            calc_dist = np.sqrt(np.square(points1[0]-points2[0])+np.square(points1[1]-points2[1]))
            print(calc_dist)
            print("p1",points1[0],points1[1])
            print("p2",points2[0],points2[1])
            if calc_dist <= dist:
                img1nooverlap = np.delete(img1nooverlap, index1, 0)
                img2nooverlap = np.delete(img2nooverlap, index2, 0)
                #img1nooverlap = img1nooverlap[~np.all(img1nooverlap == points1, axis=1)]
                #img2nooverlap = img2nooverlap[~np.all(img2nooverlap == points2, axis=1)]

   
    img1nooverlap = img1nooverlap.reshape(len(img1nooverlap), 1, 2)
    img2nooverlap = img2nooverlap.reshape(len(img2nooverlap), 1, 2)
    
    asdf = cv2.drawContours(cv2.imread('images\\background.jpg'), img1nooverlap, -1, (0, 0, 255), 25)
    displayimg.img_show(asdf)
    
test1 = np.array([[[[600, 500]], [[600, 600]], [[600, 750]], [[601,706]]]])  
#test1 = np.load('test1contours.npy')

test2 =np.array([[[[700, 300]], [[700, 400]], [[601, 701]]]])
#test2 = np.load('test2contours.npy')

find_intersection(test1,test2,dist = 3)




'''
    for index1,points1 in enumerate(img1points):
        for index2,points2 in enumerate(img2points):
            if np.array_equal(points1,points2):
                print(points1[1])
                print(points1)
                img1nooverlap = np.delete(img1points, index1, axis = 0)
                img2nooverlap = np.delete(img2points, index2, axis = 0)
'''

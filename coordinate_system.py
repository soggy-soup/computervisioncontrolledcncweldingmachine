import cv2
import numpy as np
from util_funcs import displayimg

#delete later
camera_matrix = np.load('calibration\\14%_camera_matrix.npy')
dist_coeffs = np.load('calibration\\14%_dist_coeffs.npy')

def find_aruco_corners(img, camera_matrix,dist_coeffs):
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    img = cv2.imread(img)
    undistorted_image = cv2.undistort(img, camera_matrix, dist_coeffs)
    params = cv2.aruco.DetectorParameters()
    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(undistorted_image, aruco_dict, parameters= params)
    #print(marker_corners)
    return marker_corners
    
def transform_points(corners, path):
    x,y = path[0][0][0]
    x1,y1 = [10,10] #corners[0][0][0]
    x2,y2 = [10.001,5]  #corners[0][0][1]
    theta = np.arctan((y1-y2)/(x1-x2)) #*(180/np.pi)
    print(theta)
    
    
    x_transformed = ((x-x2)*np.cos(theta)) + ((y2-y)*np.sin(theta))
    y_transformed = (-(x-x2)*np.cos(theta)) + ((y2-y)*np.sin(theta))
    
    print(x_transformed)
    print(y_transformed)
    
corners = find_aruco_corners("images\\both_w_tag.jpg",camera_matrix, dist_coeffs)
transform_points(corners, np.load("INTERSECTION.npy"))



#rect = cv2.aruco.drawDetectedMarkers(undistorted_image,marker_corners, marker_ids, None)       
#newpt = marker_corners[2][0][3] + (-7)*(marker_corners[2][0][2]-marker_corners[2][0][3])
#newpt = tuple(map(int,tuple(newpt)))
#stpt =tuple(map(int,tuple(marker_corners[2][0][3])))
#coordinatesys = cv2.line(undistorted_image, newpt,stpt,(0,0,255), 5)
#displayimg.img_show(coordinatesys)
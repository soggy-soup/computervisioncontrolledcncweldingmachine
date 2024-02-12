#import cv2
import numpy as np
import weld_joint
#import grbl_gcode
import util_funcs.displayimg

img1 = "images\\left_w_tag.jpg"
img2 = "images\\both_w_tag.jpg"

#camera distortion coefficients
mtx = np.load("calibration\\14%_camera_matrix.npy")
dst = np.load("calibration\\14%_camera_coeffs.npy")


#find aruco tag origin
corners = weld_joint.find_aruco_corners(img1,mtx,dst)
print(corners)

#find 1st contour
path1 = weld_joint.process_img(img1)
path1.img_crop(500,2500,500,3800)
path1.img_bilateral_blur()
path1.img_detect_HSV_contours() 
path1.img_draw_contours()
util_funcs.displayimg.img_show(path1.img_in_processing)

#find 2nd contour
path2 = weld_joint.process_img(img2)
path2.img_crop(500,2500,500,3800)
path2.img_bilateral_blur()
path2.img_detect_HSV_contours()
path2.img_draw_contours()
util_funcs.displayimg.img_show(path2.img_in_processing)








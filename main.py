import cv2
import numpy as np
import weld_joint
import grbl_gcode
import util_funcs.displayimg

img1 = "images\\test.jpg"
img2 = "images\\testboth.jpg"

#camera distortion coefficients
#mtx = np.load("calibration\\14%_camera_matrix.npy")
#dst = np.load("calibration\\14%_dist_coeffs.npy")
mtx = np.array([[1,0,1],[0,1,1],[0,0,1]])
dst = np.array([[1,1,1,1,1]])

#find aruco tag origin
corners1 = weld_joint.find_aruco_corners(img1,mtx,dst)

#maybe use for weighted average
#corners2 = weld_joint.find_aruco_corners(img2,mtx,dst)

#ratio = weld_joint.mm_to_px_ratio(corners1, aruco_size_mm=47.53)

#find 1st contour
path1 = weld_joint.process_img(img1)
path1.img_crop(100,3496,500,3496)
path1.img_bilateral_blur()
path1.img_detect_HSV_contours() 
path1.largest_contour()
path1.img_draw_contours()
 
util_funcs.displayimg.img_show(path1.img_in_processing)

#find 2nd contour
path2 = weld_joint.process_img(img2)
path2.img_crop(100,3496,500,3496)
path2.img_bilateral_blur()
path2.img_detect_HSV_contours()
path2.largest_contour()
path2.img_draw_contours()
util_funcs.displayimg.img_show(path2.img_in_processing)


intersection = weld_joint.radius_intersect(path1.contours,path2.contours, radius = 5)
print(type(intersection))

overlap = cv2.drawContours(cv2.imread(img2), intersection, -1, (0, 0, 255),lineType=cv2.LINE_AA, thickness = 3)

util_funcs.displayimg.img_show(overlap)

path_wrt_aruco = weld_joint.transform_points(intersection,corners1)


grbl_gcode.generate_path_gcode(path_wrt_aruco,.1205, 1600,None)




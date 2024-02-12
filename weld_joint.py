import cv2
import numpy as np

class process_img:
    def __init__(self, img_path):
        self.img_read = cv2.imread(img_path)
        
        self.img_in_processing = self.img_read
        self.contours = []
        self.heirarchy = []
        self.gray = []
        self.saturate = []
        self.thresh = []

    def img_crop(self, h_start,h_end, w_start,w_end):
        self.h_start = h_start
        self.h_end = h_end
        self.w_start = w_start
        self.w_end = w_end
        self.crop_height = slice(h_start,h_end)
        self.crop_width = slice(w_start,w_end)
        #self.img_in_processing = self.img_in_processing[self.crop_height, self.crop_width]

    def img_gaussian_blur(self):
        self.img_in_processing = cv2.GaussianBlur(self.img_in_processing, (21, 21), 0)

    def img_median_blur(self):
        self.img_in_processing = cv2.medianBlur(self.img_in_processing, 5)

    def img_bilateral_blur(self):
        self.img_in_processing = cv2.bilateralFilter(self.img_in_processing, 11, 175, 175)

    def img_basic_blur(self):
        self.img_in_processing = cv2.blur(self.img_in_processing, (100, 100))

    def img_detect_GRAY_contours(self):
        self.gray = cv2.cvtColor(self.img_in_processing, cv2.COLOR_RGB2GRAY)
        _, self.thresh = cv2.threshold(self.gray, 110, 255, cv2.THRESH_BINARY)  # 0-255, 0-black, 255-white https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
        # self.thresh = cv2. adaptiveThreshold(self.gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11,2)

        self.contours, self.heirarchy = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    def img_detect_HSV_contours(self):
        self.saturate = cv2.cvtColor(self.img_in_processing, cv2.COLOR_RGB2HSV)
        self.thresh = cv2.inRange(self.saturate, (0,100,0), (50,255,200))
        self.thresh = cv2.morphologyEx(self.thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
        self.contours, self.heirarchy = cv2.findContours(self.thresh[self.crop_height, self.crop_width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, offset=(self.w_start, self.h_start))
        self.contours = np.array(self.contours)
        
    def img_draw_contours(self):
        self.img_in_processing = cv2.drawContours(self.img_read, self.contours, -1, (0, 0, 255), thickness = 3)

def radius_intersect(cont1, cont2, radius = None):
    #radial tolerance for what is considered an "intersection", squared to reduce calcs below
    rad_squared = radius ** 2
    
    #resizing arrays to make math easier
    cont1 = cont1.squeeze()
    cont2 = cont2.squeeze()
        
    #find deltaX/deltaY and calculate distance between all points
    deltas = cont1[:,None,:] - cont2[None,:,:]
    distances = np.sum(np.square(deltas), axis = -1)
       
    #find index of coordinates that are within the overlap range
    overlap = np.flatnonzero(distances <= rad_squared)
    idx_delete = np.unravel_index(overlap,distances.shape)
        
    #delete any points that are within the overlap range
    cont1 = np.delete(cont1, idx_delete[0], 0)
    cont2 = np.delete(cont2, idx_delete[1], 0)
    
    #resize contours to 4D array to plot with openCV
    cont1 = cont1[None,:,None]
    cont2 = cont2[None,:,None]
    
    #contour containing "weld joint"
    intersection_contour = cont1

    return intersection_contour

def find_aruco_corners(img,camera_matrix,dist_coeffs):
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    img = cv2.imread(img)
    undistorted_image = cv2.undistort(img, camera_matrix, dist_coeffs)
    params = cv2.aruco.DetectorParameters()
    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(undistorted_image, aruco_dict, parameters= params)

    return marker_corners
    
def transform_points(path, corners):
    x1,y1 = corners[0][0][1]
    x2,y2 = corners[0][0][2]
    theta = np.arctan((y1-y2)/(x1-x2)) 

    path[:,:,:,0] = ((path[:,:,:,0]-x2)*np.cos(theta))+((y2-path[:,:,:,1])*np.sin(theta))   
    path[:,:,:,1] = (-(path[:,:,:,0]-x2)*np.cos(theta))+((y2-path[:,:,:,1])*np.sin(theta))   
    transformed_path = path
    
    return transformed_path





















import cv2
import numpy as np
# https://www.youtube.com/watch?v=FczN93nT-dQ
# https://www.youtube.com/watch?v=aFNDh5k3SjU
# https://docs.opencv.org/4.9.0/d2/de8/group__core__array.html#ga303cfb72acf8cbb36d884650c09a3a97
# camera calibration mtx/dist matricies
mtx = np.loadtxt('calibration\\mtx.txt')
dist = np.loadtxt('calibration\\dist.txt')

def img_show(img_to_show):
        aspect_ratio = img_to_show.shape[1] / img_to_show.shape[0]
        cv2.namedWindow("Display Image", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.imshow("Display Image", img_to_show)

        while True:
            key = cv2.waitKey(1)
            if key == 27:
                break

            current_width = cv2.getWindowImageRect("Display Image")[2]
            new_height = int(current_width / aspect_ratio)
            cv2.resizeWindow("Display Image", current_width, new_height)
        cv2.destroyAllWindows()

class process_img:
    def __init__(self, img_path):
        self.img_read = cv2.imread(img_path)
        
        #undistorting/remapping
        h,  w = self.img_read.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
        self.img_undistorted = cv2.remap(self.img_read, mapx, mapy, cv2.INTER_LINEAR)
        
        # crop the image
        x, y, w, h = roi
        self.img_undistorted = self.img_undistorted[y:y+h, x:x+w]
        
        self.img_in_processing = self.img_undistorted
        self.contours = []
        self.heirarchy = []
        self.gray = []
        self.saturate = []
        self.thresh = []

    def img_crop(self, h_start,h_end, w_start,w_end):
        self.crop_height = slice(h_start,h_end)
        self.crop_width = slice(w_start,w_end)
        self.img_in_processing = self.img_in_processing[self.crop_height, self.crop_width]

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
        self.contours, self.heirarchy = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
    def img_draw_contours(self):
        self.img_in_processing = cv2.drawContours(self.img_undistorted[self.crop_height, self.crop_width], self.contours, -1, (0, 0, 255), 10)


test = process_img("images\\newlightingtest.jpg")
#test.img_crop(175,3300,535,3800)
test.img_crop(0,4000,0,4000)

test.img_bilateral_blur()
test.img_detect_HSV_contours()
test.img_draw_contours()

img_show(test.img_in_processing)

print(test.heirarchy)
import cv2
from util_funcs import displayimg

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
        
    def img_draw_contours(self):
        self.img_in_processing = cv2.drawContours(self.img_read, self.contours, -1, (0, 0, 255), 10)


test = process_img("images\\both.jpg")
test.img_crop(200,3300,535,3800)

test.img_bilateral_blur()
test.img_detect_HSV_contours()
test.img_draw_contours()

displayimg.img_show(test.img_in_processing)

print(test.heirarchy)
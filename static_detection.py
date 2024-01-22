import cv2

class process_img:
    def __init__(self, img_path):
        self.img_read = cv2.imread(img_path)
        self.img_in_processing = self.img_read
        self.contours = []
        self.heirarchy = []
        self.gray = []
        self.saturate = []
        self.thresh = []

    def img_show(self, img_to_show):
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

    def img_crop(self):
        self.img_in_processing = self.img_in_processing[175:3300, 535:3950]

    def img_gaussian_blur(self):
        self.img_in_processing = cv2.GaussianBlur(self.img_in_processing, (3, 3), 0)

    def img_median_blur(self):
        self.img_in_processing = cv2.medianBlur(self.img_in_processing, 5)

    def img_bilateral_blur(self):
        self.img_in_processing = cv2.bilateralFilter(self.img_in_processing, 11, 15, 15)

    def img_basic_blur(self):
        self.img_in_processing = cv2.blur(self.img_in_processing, (100, 100))

    def img_detect_GRAY_contours(self):
        self.gray = cv2.cvtColor(self.img_in_processing, cv2.COLOR_RGB2GRAY)
        _, self.thresh = cv2.threshold(self.gray, 110, 255, cv2.THRESH_BINARY)  # 0-255, 0-black, 255-white https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
        # self.thresh = cv2. adaptiveThreshold(self.gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11,2)

        self.contours, self.heirarchy = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    def img_detect_HSV_contours(self):
        self.saturate = cv2.cvtColor(self.img_in_processing, cv2.COLOR_RGB2HSV)
        self.thresh = cv2.inRange(self.saturate, (0,0,105), (180,50,255))
        self.thresh = cv2.morphologyEx(self.thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        self.contours, self.heirarchy = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
    def img_draw_contours(self,):
        self.img_in_processing = cv2.drawContours(self.img_read[175:3300, 535:3950], self.contours, -1, (0, 255, 0), 5)

#https://docs.opencv.org/4.9.0/d2/de8/group__core__array.html#ga303cfb72acf8cbb36d884650c09a3a97
test = process_img("C:\\Users\\Aidan\\Documents\\Projects\\CNC Welding Table\\CNCWelderCode\\computervisioncontrolledcncweldingmachine\\images\\othersideofplate.jpg")
test.img_crop()
test.img_bilateral_blur()
test.img_detect_HSV_contours()
test.img_show(test.thresh)
test.img_draw_contours()
test.img_show(test.img_in_processing)
print(test.heirarchy)


"""
    def img_show(self):
        aspect_ratio = self.img_in_processing.shape[1] / self.img_in_processing.shape[0]
        cv2.namedWindow("Display Image", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.imshow("Display Image", self.img_in_processing)

        while True:
            key = cv2.waitKey(1)
            if key == 27: 
                break

            current_width = cv2.getWindowImageRect("Display Image")[2]
            new_height = int(current_width / aspect_ratio)
            cv2.resizeWindow("Display Image", current_width, new_height)
        cv2.destroyAllWindows()
"""

import numpy as np
import cv2

class process_img:
    def __init__(self, img_path):
        self.img_read = cv2.imread(img_path)
        self.img_in_processing = self.img_read
        self.contours = []
        self.heirarchy = []

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
        
    def img_crop(self):
        self.img_in_processing = self.img_in_processing[175:3300, 535:3950]
    
    def img_gaussian_blur(self):
        self.img_in_processing = cv2.GaussianBlur(self.img_in_processing, (101, 101), 5)

    def img_detect_contours(self,):
        gray = cv2.cvtColor(self.img_in_processing, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
        self.contours, self.heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    def img_draw_contours(self,):
        self.img_in_processing = cv2.drawContours(self.img_read[175:3300, 535:3950], self.contours, -1, (0, 255, 0), 30)

test = process_img('C:/Users/odion/OneDrive/Documents/CAD Stuff/CNC Welding Table/New Computer Vision Code/computervisioncontrolledcncweldingmachine/images/othersideofplate.jpg')
test.img_crop()
test.img_gaussian_blur()
test.img_detect_contours()
test.img_draw_contours()
test.img_show()












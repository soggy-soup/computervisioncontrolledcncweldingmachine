import numpy as np
import cv2

class process_img:
    def __init__(self, img_path):
        self.img_read = cv2.imread(img_path)
        self.img_in_processing = self.img_read

    def img_show(self):
        cv2.imshow("Image in Processing", self.img_in_processing)

    def img_scale(self, percent = None):
        width = int(self.img_in_processing.shape[1] * percent/100)
        height = int(self.img_in_processing.shape[0] * percent/100)
        dim = (width, height)
        self.img_in_processing = cv2.resize(self.img_in_processing,dim,interpolation=cv2.INTER_AREA)



    def img_crop(self,):

a
    def img_detect_contours(self,):


    def img_draw_contours(self,):
















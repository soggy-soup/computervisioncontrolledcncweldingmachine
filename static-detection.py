import numpy as np
import cv2

class process_img:
    def __init__(self, img_path):
        self.img_read = cv2.imread(img_path)
        self.img_in_processing = self.img_read

    def img_show(self):
        aspect_ratio = self.img_in_processing.shape[1] / self.img_in_processing.shape[0]
        cv2.namedWindow("Display Image", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.imshow("Display Image", self.img_in_processing)
        
        while True:
            key = cv2.waitKey(1)
            if key == 27:  # Break the loop if 'Esc' key is pressed
                break

            current_width = cv2.getWindowImageRect("Display Image")[2]
            new_height = int(current_width / aspect_ratio)
            cv2.resizeWindow("Display Image", current_width, new_height)
        cv2.destroyAllWindows()



    def img_scale(self, percent = None):
        width = int(self.img_in_processing.shape[1] * percent/100)
        height = int(self.img_in_processing.shape[0] * percent/100)
        dim = (width, height)
        self.img_in_processing = cv2.resize(self.img_in_processing,dim,interpolation=cv2.INTER_AREA)



    #def img_crop(self,):


   # def img_detect_contours(self,):


    #def img_draw_contours(self,):

test = process_img('C:/Users/odion/OneDrive/Documents/CAD Stuff/CNC Welding Table/New Computer Vision Code/computervisioncontrolledcncweldingmachine/images/othersideofplate.jpg')

test.img_show()












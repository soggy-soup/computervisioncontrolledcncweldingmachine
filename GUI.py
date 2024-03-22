from tkinter import *
from PIL import Image, ImageTk
import cv2
import customtkinter
import numpy as np
import weld_joint
import grbl_gcode
import util_funcs.displayimg


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        #initialize window properties
        self.bind('<Escape>', lambda e: self.quit())
        self.title("CNC Welder")
        self.resizable(width=False, height=False)
        customtkinter.set_appearance_mode("dark")
        
        #initialize contours as empty
        self.contours1 = None
        self.contours2 = None
        self.joint_intersection = None
        self.path_wrt_aruco = None
        self.corners = None
        
        #switch states to ensure first picture is taken before second
        self.img1_state = NORMAL
        self.img2_state = DISABLED
        self.intersection_state = DISABLED
        
        #setup video stream with opencv      
        focus = 14
        video_width, video_height = 1280,720
        video_aspect_ratio = video_width/video_height
        tot_rows = 15
        self.cap = cv2.VideoCapture(0,cv2.CAP_MSMF)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height) 
        self.cap.set(28,focus)
        self.video_win_width, self.video_win_height = 800, int(800/video_aspect_ratio)     
        
        #create video stream label
        self.video_stream = customtkinter.CTkLabel(self,text="")
        self.video_stream.grid(row=0,column=0, padx=10,pady=10,rowspan=tot_rows)
        
        #frame for all button controls
        right_frame = customtkinter.CTkFrame(self, width=600, height=self.video_win_height)
        right_frame.grid(row=0,column=1,padx=10,pady=10,columnspan=3,rowspan=tot_rows)


        #image processing buttons
        customtkinter.CTkLabel(self, text="Joint Detection:").grid(row=2,column=1)
        self.img1 = customtkinter.CTkButton(self,text="Picture 1",fg_color="red",state=self.img1_state, command=self.process_img1).grid(row=3,column=1)
        self.img2 = customtkinter.CTkButton(self,text="Picture 2",fg_color="blue",state=self.img2_state,command=self.process_img2).grid(row=3,column=2)
        self.joint_location = customtkinter.CTkButton(self,text="Weld Joint",state=self.intersection_state,command = self.joint).grid(row=3,column=3)
            
        self.open_camera()
        

    def open_camera(self):
        _, self.frame = self.cap.read()
        cv2_img = cv2.drawContours(self.frame, self.contours1, -1, (0,0,255), thickness = 7)
        cv2_img = cv2.drawContours(cv2_img, self.contours2, -1, (0,255,0), thickness = 7)
        cv2_img = cv2.drawContours(cv2_img, self.joint_intersection, -1, (255,0,0), thickness = 7)
        cv2_img =  cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGBA)
        cap_img = Image.fromarray(cv2_img)
        photo_img = customtkinter.CTkImage(light_image=cap_img,size=(self.video_win_width,self.video_win_height))
        self.video_stream.photo_img = photo_img
        self.video_stream.configure(image =photo_img)
        self.video_stream.after(10,self.open_camera)

    def process_img1(self):
        path = weld_joint.process_img(None)
        path.img_in_processing = self.frame
        path.img_crop(100,3496,500,3496)
        path.img_bilateral_blur()
        path.img_detect_HSV_contours() 
        path.largest_contour()
        
        #empty distortion matrix because camera has negligeble distortion
        mtx = np.array([[1,0,1],[0,1,1],[0,0,1]])
        dst = np.array([[1,1,1,1,1]])
        
        self.corners = weld_joint.find_aruco_corners(self.frame,mtx,dst)
        self.contours2 = None
        self.joint_intersection = None
        self.contours1 = path.contours
        
        self.img2_state = NORMAL
        self.grid_slaves(row=3, column=2)[0].configure(state=self.img2_state)
        self.intersection_state = DISABLED
        self.grid_slaves(row=3, column=3)[0].configure(state=self.intersection_state)
        
    def process_img2(self):
        path = weld_joint.process_img(None)
        path.img_in_processing = self.frame
        path.img_crop(100,3496,500,3496)
        path.img_bilateral_blur()
        path.img_detect_HSV_contours() 
        path.largest_contour()
        
        self.joint_intersection = None
        self.contours2 = path.contours
        
        self.img2_state = DISABLED
        self.intersection_state = NORMAL
        self.grid_slaves(row=3, column=2)[0].configure(state=self.img2_state)
        self.grid_slaves(row=3, column=3)[0].configure(state=self.intersection_state)
    
    def joint(self):
        if ((self.contours1 is not None) & (self.contours2 is not None) & (self.corners is not None)):
            self.joint_intersection = weld_joint.radius_intersect(self.contours1,self.contours2,radius=3)
            #self.path_wrt_aruco = weld_joint.transform_points(self.joint_intersection, self.corners)
            self.intersection_state = DISABLED
            self.grid_slaves(row=3, column=3)[0].configure(state=self.intersection_state)
            self.contours1 = None
            self.contours2 = None
                    
    def gcode(self):
        if (self.path_wrt_aruco is not None):
            grbl_gcode.generate_path_gcode(self.path_wrt_aruco,0.1205, 300)
         
        



app = App()
app.mainloop()

